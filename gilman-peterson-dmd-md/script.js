// Marks today's row in the hours table and shows today's hours under the phone number.
(function () {
  var day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][new Date().getDay()];
  var row = document.querySelector('.hours tr[data-day="' + day + '"]');
  if (!row) return;
  row.classList.add("today");
  var cell = row.querySelector("td");
  var line = document.getElementById("today-hours");
  if (cell && line) {
    line.textContent = "Today: " + cell.textContent.trim();
    line.hidden = false;
  }
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
