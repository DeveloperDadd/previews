// Marks today's row in the hours table and shows the preview note when the form is sent.
(function () {
  var day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][new Date().getDay()];
  var row = document.querySelector('.hours tr[data-day="' + day + '"]');
  if (row) row.classList.add("today");
  var form = document.getElementById("quote-form");
  var note = document.getElementById("form-note");
  if (form && note) form.addEventListener("submit", function (e) {
    e.preventDefault();
    note.hidden = false;
    note.focus();
  });
})();
