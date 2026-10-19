(() => {
  "use strict";
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#nav-links");
  const year = document.querySelector("#year");
  if (year) year.textContent = String(new Date().getFullYear());
  if (!toggle || !nav) return;
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    nav.classList.toggle("is-open", !open);
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = open ? "Apri navigazione" : "Chiudi navigazione";
  });
  nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Apri navigazione";
  }));
})();