(function () {
  const OPEN_COLLECTIVE_CHECKOUT_URL =
    "https://opencollective.com/datalets/projects/public-ai-switzerland/contribute/founding-membership-99202/checkout?interval=year&amount=100&contributeAs=me";

  function initJoinLinks() {
    document.querySelectorAll(".js-join-link").forEach((link) => {
      link.setAttribute("href", OPEN_COLLECTIVE_CHECKOUT_URL);
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initJoinLinks);
  } else {
    initJoinLinks();
  }
})();
