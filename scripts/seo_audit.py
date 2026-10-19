#!/usr/bin/env python3
"""Dependency-free static SEO audit for HTML websites and repository site roots."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

SKIP_DIRS = {".git", ".seo-framework", "node_modules", "vendor", ".next", ".nuxt", "coverage"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.description = ""
        self.lang = ""
        self.canonicals: list[str] = []
        self.og_title = ""
        self.og_description = ""
        self.og_image = ""
        self.twitter_card = ""
        self.h1_count = 0
        self.images_missing_alt = 0
        self.jsonld_raw: list[str] = []
        self._in_jsonld = False
        self._jsonld_parts: list[str] = []
        self.local_refs: list[str] = []
        self.robots_meta = ""
        self.meta_robots = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "").strip() for k, v in attrs if k}
        tag = tag.lower()
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            if "alt" not in a:
                self.images_missing_alt += 1
            if a.get("src"):
                self.local_refs.append(a["src"])

        if tag == "meta":
            name = a.get("name", "").lower()
            prop = a.get("property", "").lower()
            content = a.get("content", "").strip()
            if name == "description":
                self.description = content
            elif name == "robots":
                self.robots_meta = content
                self.meta_robots = "noindex" in content.lower()
            elif name == "twitter:card":
                self.twitter_card = content
            elif prop == "og:title" or name == "og:title":
                self.og_title = content
            elif prop == "og:description" or name == "og:description":
                self.og_description = content
            elif prop == "og:image" or name == "og:image":
                self.og_image = content
        elif tag == "link":
            rel = set(a.get("rel", "").lower().split())
            if "canonical" in rel and a.get("href"):
                self.canonicals.append(a["href"])
            if a.get("href"):
                self.local_refs.append(a["href"])
        elif tag in {"a", "script", "source", "video", "audio", "iframe"}:
            for key in ("href", "src", "poster"):
                if a.get(key):
                    self.local_refs.append(a[key])
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self._in_jsonld:
            self._jsonld_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self._in_jsonld:
            self.jsonld_raw.append("".join(self._jsonld_parts).strip())
            self._in_jsonld = False
            self._jsonld_parts = []

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.title_parts)).strip()


def add_issue(issues: list[dict[str, str]], severity: str, path: str, message: str) -> None:
    issues.append({"severity": severity, "path": path, "message": message})


def is_external_or_fragment(ref: str) -> bool:
    value = ref.strip()
    if not value or value.startswith("#") or value.startswith("//"):
        return True
    return bool(urlsplit(value).scheme) or value.startswith(("data:", "javascript:"))


def resolve_local_ref(root: Path, page: Path, ref: str) -> Path | None:
    if is_external_or_fragment(ref):
        return None
    parts = urlsplit(ref.strip())
    if not parts.path:
        return None
    raw_path = unquote(parts.path)
    candidate = root / raw_path.lstrip("/") if raw_path.startswith("/") else page.parent / raw_path
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if candidate.is_dir():
        candidate = candidate / "index.html"
    if candidate.exists():
        return candidate
    if not candidate.suffix:
        for alternate in (candidate.with_suffix(".html"), candidate / "index.html"):
            if alternate.exists():
                return alternate
    return candidate


def check_page(root: Path, page: Path, issues: list[dict[str, str]], check_links: bool) -> None:
    rel = page.relative_to(root).as_posix()
    try:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        parser.close()
    except Exception as exc:
        add_issue(issues, "ERROR", rel, f"HTML parsing failed: {exc}")
        return

    if not parser.title:
        add_issue(issues, "ERROR", rel, "Missing or empty title element.")
    elif len(parser.title) < 20 or len(parser.title) > 70:
        add_issue(issues, "WARN", rel, f"Title length is {len(parser.title)} characters; review clarity and SERP truncation (heuristic target 20–70).")

    if not parser.description:
        add_issue(issues, "WARN", rel, "Missing meta description.")
    elif len(parser.description) < 60 or len(parser.description) > 180:
        add_issue(issues, "INFO", rel, f"Meta description is {len(parser.description)} characters; review truncation and coverage (heuristic target 60–180).")

    if not parser.lang:
        add_issue(issues, "WARN", rel, "Missing html lang attribute.")
    elif not re.match(r"^[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*$", parser.lang):
        add_issue(issues, "WARN", rel, f"Unusual html lang value: {parser.lang!r}.")

    if not parser.canonicals:
        add_issue(issues, "WARN", rel, "Missing rel=canonical; review whether a self-referencing canonical is needed.")
    elif len(parser.canonicals) > 1:
        add_issue(issues, "ERROR", rel, f"Found {len(parser.canonicals)} canonical tags; keep one authoritative canonical.")
    else:
        canonical = urlsplit(parser.canonicals[0])
        if canonical.scheme not in {"http", "https"} or not canonical.netloc:
            add_issue(issues, "ERROR", rel, f"Canonical is not an absolute HTTP(S) URL: {parser.canonicals[0]!r}.")

    if parser.h1_count == 0:
        add_issue(issues, "WARN", rel, "No H1 heading found.")
    elif parser.h1_count > 1:
        add_issue(issues, "INFO", rel, f"Found {parser.h1_count} H1 headings; verify the primary heading and semantic hierarchy.")

    if parser.images_missing_alt:
        add_issue(issues, "WARN", rel, f"{parser.images_missing_alt} image(s) lack an alt attribute. Use meaningful text for informative images and alt=\"\" for decorative images.")

    missing_og = [name for name, value in (
        ("og:title", parser.og_title),
        ("og:description", parser.og_description),
        ("og:image", parser.og_image),
    ) if not value]
    if missing_og:
        add_issue(issues, "INFO", rel, "Open Graph metadata to review: " + ", ".join(missing_og) + ".")

    if not parser.twitter_card:
        add_issue(issues, "INFO", rel, "twitter:card is absent; optional social-preview enhancement.")

    if parser.meta_robots:
        add_issue(issues, "INFO", rel, f"Page contains robots noindex directive: {parser.robots_meta!r}; verify that exclusion is intentional.")

    for raw in parser.jsonld_raw:
        if not raw:
            add_issue(issues, "ERROR", rel, "Empty JSON-LD script block.")
            continue
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            add_issue(issues, "ERROR", rel, f"Invalid JSON-LD: {exc.msg} at character {exc.pos}.")

    if check_links:
        for ref in dict.fromkeys(parser.local_refs):
            target = resolve_local_ref(root, page, ref)
            if target is None or is_external_or_fragment(ref):
                continue
            if not target.exists():
                try:
                    checked = target.relative_to(root).as_posix()
                except ValueError:
                    checked = target.name
                add_issue(issues, "INFO", rel, f"Local reference may not resolve: {ref!r} (checked {checked}).")


def check_robots(root: Path, robots_rel: str, sitemap_rel: str, issues: list[dict[str, str]]) -> None:
    robots = root / robots_rel
    sitemap = root / sitemap_rel
    if not robots.is_file():
        add_issue(issues, "WARN", robots_rel, "robots.txt not found at the configured site root.")
        return
    text = robots.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        if re.match(r"(?i)^disallow\s*:\s*/\s*$", value):
            add_issue(issues, "ERROR", robots_rel, f"Potential site-wide crawl block: {value!r}. Confirm that it is intentional.")
    sitemap_lines = [line.split(":", 1)[1].strip() for line in text.splitlines() if line.strip().lower().startswith("sitemap:")]
    if sitemap.is_file() and not sitemap_lines:
        add_issue(issues, "WARN", robots_rel, f"robots.txt exists but does not reference {sitemap_rel}.")
    if len(sitemap_lines) > 1:
        add_issue(issues, "INFO", robots_rel, f"robots.txt declares {len(sitemap_lines)} sitemaps; verify that all are intended.")


def check_sitemap(root: Path, sitemap_rel: str, issues: list[dict[str, str]]) -> int:
    sitemap = root / sitemap_rel
    if not sitemap.is_file():
        add_issue(issues, "WARN", sitemap_rel, "XML sitemap not found at the configured site root.")
        return 0
    try:
        tree = ET.parse(sitemap)
    except (ET.ParseError, OSError) as exc:
        add_issue(issues, "ERROR", sitemap_rel, f"Sitemap XML cannot be parsed: {exc}.")
        return 0
    locs = [element.text.strip() for element in tree.getroot().iter()
            if element.tag.lower().endswith("loc") and element.text and element.text.strip()]
    if not locs:
        add_issue(issues, "WARN", sitemap_rel, "Sitemap contains no loc URLs.")
    duplicates = [url for url, count in Counter(locs).items() if count > 1]
    if duplicates:
        add_issue(issues, "ERROR", sitemap_rel, f"Sitemap has {len(duplicates)} duplicate URL(s).")
    for loc in locs:
        parsed = urlsplit(loc)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            add_issue(issues, "ERROR", sitemap_rel, f"Sitemap URL is not absolute HTTP(S): {loc!r}.")
            break
    return len(locs)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a static, dependency-free SEO hygiene audit.")
    ap.add_argument("--root", default=".", help="Published site root (default: current directory).")
    ap.add_argument("--robots", default="robots.txt", help="robots.txt path relative to --root.")
    ap.add_argument("--sitemap", default="sitemap.xml", help="sitemap.xml path relative to --root.")
    ap.add_argument("--check-links", action="store_true", help="Check local links and asset references; base-path routes can produce advisory findings.")
    ap.add_argument("--strict", action="store_true", help="Return nonzero when ERROR findings exist.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: site root does not exist: {root}", file=sys.stderr)
        return 2

    issues: list[dict[str, str]] = []
    pages = sorted(
        path for path in root.rglob("*.html")
        if not any(part in SKIP_DIRS or part.startswith(".") for part in path.relative_to(root).parts)
    )
    if not pages:
        add_issue(issues, "ERROR", ".", "No HTML pages found under the configured site root.")
    if not (root / "index.html").is_file():
        add_issue(issues, "WARN", "index.html", "No index.html at the configured root; verify the selected publish directory.")

    title_paths: dict[str, list[str]] = defaultdict(list)
    description_paths: dict[str, list[str]] = defaultdict(list)
    canonical_paths: dict[str, list[str]] = defaultdict(list)

    for page in pages:
        check_page(root, page, issues, args.check_links)
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        parser.close()
        rel = page.relative_to(root).as_posix()
        if parser.title:
            title_paths[parser.title.casefold()].append(rel)
        if parser.description:
            description_paths[re.sub(r"\s+", " ", parser.description).strip().casefold()].append(rel)
        for canonical in set(parser.canonicals):
            canonical_paths[canonical].append(rel)

    for title, paths in title_paths.items():
        if len(paths) > 1:
            add_issue(issues, "WARN", "site-wide", f"Duplicate title used by {len(paths)} pages: {title!r} — " + ", ".join(paths[:8]))
    for description, paths in description_paths.items():
        if len(paths) > 1:
            add_issue(issues, "INFO", "site-wide", f"Duplicate meta description used by {len(paths)} pages — " + ", ".join(paths[:8]))
    for canonical, paths in canonical_paths.items():
        if len(paths) > 1:
            add_issue(issues, "WARN", "site-wide", f"Same canonical URL appears on {len(paths)} pages: {canonical!r} — " + ", ".join(paths[:8]))

    check_robots(root, args.robots, args.sitemap, issues)
    sitemap_urls = check_sitemap(root, args.sitemap, issues)

    counts = Counter(row["severity"] for row in issues)
    print("SEO STATIC AUDIT")
    print(f"Site root: {root}")
    print(f"HTML pages scanned: {len(pages)}")
    print(f"URLs in sitemap: {sitemap_urls}")
    print("Findings: " + ", ".join(f"{key}={counts.get(key, 0)}" for key in ("ERROR", "WARN", "INFO")))
    for row in issues:
        print(f"[{row['severity']}] {row['path']}: {row['message']}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write("# Static SEO audit\n\n")
            handle.write(f"- **Site root:** {args.root}\n- **HTML pages scanned:** {len(pages)}\n- **URLs in sitemap:** {sitemap_urls}\n")
            handle.write(f"- **Findings:** {counts.get('ERROR', 0)} error(s), {counts.get('WARN', 0)} warning(s), {counts.get('INFO', 0)} info item(s)\n\n")
            if issues:
                handle.write("| Severity | Path | Finding |\n|---|---|---|\n")
                for row in issues[:150]:
                    message = row["message"].replace("|", "\\|").replace("\n", " ")
                    handle.write(f"| {row['severity']} | {row['path']} | {message} |\n")
                if len(issues) > 150:
                    handle.write(f"\n_Only the first 150 of {len(issues)} findings are shown._\n")
            else:
                handle.write("No findings from the configured static checks.\n")

    return 1 if args.strict and counts.get("ERROR", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
