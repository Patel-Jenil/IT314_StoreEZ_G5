"use strict";

const startDateEl = document.getElementById("startDate");
const endDateEl = document.getElementById("endDate");

let date = new Date();

let tdate = date.getDate();
let month = date.getMonth() + 1;
let year = date.getUTCFullYear();

if (tdate < 10) {
	tdate = "0" + tdate;
}

if (month < 10) {
	month = "0" + month;
}

let startDate = year + "-" + month + "-" + tdate;
startDateEl.setAttribute("min", startDate);

endDateEl.addEventListener("click", function () {
	const endDate = $("#startDate").val();
	endDateEl.setAttribute("min", endDate);
});
