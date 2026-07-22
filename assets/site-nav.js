(function () {
  function closeNav(nav, toggle) {
    nav.classList.remove("site-nav--open");
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("site-nav-menu-open");
  }

  function openNav(nav, toggle) {
    nav.classList.add("site-nav--open");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("site-nav-menu-open");
  }

  function initSiteNav() {
    document.querySelectorAll(".site-nav").forEach((nav) => {
      const toggle = nav.querySelector(".site-nav__toggle");
      const links = nav.querySelector("#site-menu");
      const backdrop = nav.querySelector(".site-nav__backdrop");

      if (!toggle || !links) {
        return;
      }

      toggle.addEventListener("click", () => {
        const isOpen = nav.classList.contains("site-nav--open");
        if (isOpen) {
          closeNav(nav, toggle);
        } else {
          openNav(nav, toggle);
        }
      });

      if (backdrop) {
        backdrop.addEventListener("click", () => {
          closeNav(nav, toggle);
        });
      }

      links.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
          closeNav(nav, toggle);
        });
      });

      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && nav.classList.contains("site-nav--open")) {
          closeNav(nav, toggle);
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSiteNav);
  } else {
    initSiteNav();
  }
})();
