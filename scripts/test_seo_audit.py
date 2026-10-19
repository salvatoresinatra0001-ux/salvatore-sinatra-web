from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import seo_audit


class SeoAuditTests(unittest.TestCase):
    def test_parser_reads_basic_metadata(self):
        html = """<!doctype html>
        <html lang="it">
          <head>
            <title>Portfolio fotografico — Salvatore Sinatra</title>
            <meta name="description" content="Portfolio fotografico d'autore, ritratti, paesaggio e ricerca visiva in Sicilia.">
            <link rel="canonical" href="https://example.test/">
            <meta property="og:title" content="Salvatore Sinatra">
            <meta property="og:description" content="Fotografia Fine Art">
            <meta property="og:image" content="https://example.test/cover.jpg">
          </head>
          <body><h1>Fotografia d'autore</h1><img src="/photo.jpg" alt="Ritratto in bianco e nero"></body>
        </html>"""
        parser = seo_audit.PageParser()
        parser.feed(html)
        parser.close()
        self.assertEqual(parser.lang, "it")
        self.assertEqual(parser.title, "Portfolio fotografico — Salvatore Sinatra")
        self.assertEqual(parser.canonicals, ["https://example.test/"])
        self.assertEqual(parser.h1_count, 1)
        self.assertEqual(parser.images_missing_alt, 0)
        self.assertEqual(parser.og_image, "https://example.test/cover.jpg")

    def test_parser_captures_valid_jsonld(self):
        source = '<html><head><script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"Example"}</script></head></html>'
        parser = seo_audit.PageParser()
        parser.feed(source)
        parser.close()
        self.assertEqual(len(parser.jsonld_raw), 1)
        self.assertEqual(json.loads(parser.jsonld_raw[0])["@type"], "Person")

    def test_sitemap_checks_absolute_urls_and_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sitemap.xml").write_text(
                '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                '<url><loc>https://example.test/</loc></url>'
                '<url><loc>https://example.test/about/</loc></url></urlset>',
                encoding="utf-8",
            )
            issues = []
            count = seo_audit.check_sitemap(root, "sitemap.xml", issues)
            self.assertEqual(count, 2)
            self.assertEqual(issues, [])

    def test_sitemap_rejects_malformed_xml(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sitemap.xml").write_text("<urlset><url>", encoding="utf-8")
            issues = []
            count = seo_audit.check_sitemap(root, "sitemap.xml", issues)
            self.assertEqual(count, 0)
            self.assertTrue(any(item["severity"] == "ERROR" for item in issues))


if __name__ == "__main__":
    unittest.main()
