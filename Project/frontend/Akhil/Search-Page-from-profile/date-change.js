document.addEventListener("DOMContentLoaded", function () {
  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");

  // Set the minimum end date based on the selected start date
  startDateInput.addEventListener("change", function () {
      endDateInput.min = startDateInput.value;
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");

  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();

  const currentYearMinDate = `${currentYear}-01-01`;
  const currentYearMaxDate = `${currentYear}-12-31`;

  startDateInput.min = currentYearMinDate;
  startDateInput.max = currentYearMaxDate;

  endDateInput.min = currentYearMinDate;
  endDateInput.max = currentYearMaxDate;
});