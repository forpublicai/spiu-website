(function () {
  const LOCALES = [
    { id: "en", label: "EN", hreflang: "en" },
    { id: "de", label: "DE", hreflang: "de-CH" },
    { id: "fr", label: "FR", hreflang: "fr-CH" },
    { id: "it", label: "IT", hreflang: "it-CH" },
    { id: "rm", label: "RM", hreflang: "rm-CH" },
  ];

  function parsePath() {
    const segments = window.location.pathname
      .replace(/\/$/, "")
      .split("/")
      .filter(Boolean);

    const localeIds = ["de", "fr", "it", "rm"];
    let locale = "en";
    let page = "index.html";

    if (segments.length && localeIds.includes(segments[0])) {
      locale = segments[0];
      page = segments[1] || "index.html";
    } else if (segments.length) {
      page = segments[segments.length - 1].endsWith(".html")
        ? segments[segments.length - 1]
        : "index.html";
    }

    return { locale, page };
  }

  function localeHref(locale, page) {
    const isHome = page === "index.html";
    if (locale === "en") {
      return isHome ? "/" : `/${page}`;
    }
    return isHome ? `/${locale}/` : `/${locale}/${page}`;
  }

  function mount() {
    const mountPoint = document.querySelector("[data-lang-switcher]");
    if (!mountPoint || mountPoint.querySelector(".lang-switcher")) {
      return;
    }

    const { locale, page } = parsePath();
    const current =
      LOCALES.find(({ id }) => id === locale) || LOCALES[0];

    const switcher = document.createElement("details");
    switcher.className = "lang-switcher";

    const toggle = document.createElement("summary");
    toggle.className = "lang-switcher__toggle";
    toggle.setAttribute("aria-label", "Language");
    toggle.innerHTML =
      `<span class="lang-switcher__label">${current.label}</span>` +
      '<span class="lang-switcher__chevron" aria-hidden="true"></span>';

    const menu = document.createElement("div");
    menu.className = "lang-switcher__menu";
    menu.setAttribute("role", "listbox");
    menu.setAttribute("aria-label", "Language");

    LOCALES.forEach(({ id, label, hreflang }) => {
      if (id === locale) {
        return;
      }

      const link = document.createElement("a");
      link.href = localeHref(id, page);
      link.textContent = label;
      link.lang = hreflang;
      link.hreflang = hreflang;
      link.setAttribute("role", "option");
      menu.appendChild(link);
    });

    switcher.appendChild(toggle);
    switcher.appendChild(menu);
    mountPoint.appendChild(switcher);

    toggle.setAttribute("aria-expanded", "false");

    switcher.addEventListener("toggle", () => {
      toggle.setAttribute(
        "aria-expanded",
        switcher.open ? "true" : "false"
      );
    });

    document.addEventListener("click", (event) => {
      if (!switcher.open || switcher.contains(event.target)) {
        return;
      }
      switcher.open = false;
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && switcher.open) {
        switcher.open = false;
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
