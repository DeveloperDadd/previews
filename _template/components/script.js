// Marks today's row in the footer hours.
(function () {
  var day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][new Date().getDay()];
  var row = document.querySelector('.cs-hours-row[data-day="' + day + '"]');
  if (row) row.classList.add("today");
})();

// Small-screen menu (from components/nav/cs-navigation): opens and closes the link list.
(function () {
  var nav = document.getElementById("cs-navigation");
  var toggle = nav && nav.querySelector(".cs-toggle");
  if (!toggle) return;
  function setOpen(open) {
    nav.classList.toggle("cs-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }
  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });
  nav.querySelectorAll(".cs-li-link").forEach(function (link) {
    link.addEventListener("click", function () { setOpen(false); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.classList.contains("cs-open")) {
      setOpen(false);
      toggle.focus();
    }
  });
})();
