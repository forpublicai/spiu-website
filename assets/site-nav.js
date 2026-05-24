(function () {
  function initSiteNav() {
    document.querySelectorAll(".site-nav").forEach((nav) => {
      const toggle = nav.querySelector(".site-nav__toggle");
      const links = nav.querySelector("#site-menu");

      if (!toggle || !links) {
        return;
      }

      toggle.addEventListener("click", () => {
        const isOpen = nav.classList.toggle("site-nav--open");
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSiteNav);
  } else {
    initSiteNav();
  }
})();
