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
