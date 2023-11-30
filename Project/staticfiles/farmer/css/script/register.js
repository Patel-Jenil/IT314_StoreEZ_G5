"use strict";

const latitudeEl = document.getElementById("latitude");
const longitudeEl = document.getElementById("longitude");

const detectButton = document.querySelector(".button-8");

detectButton.addEventListener("click", function () {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition((position) => {
			const { latitude, longitude } = position.coords;
			latitudeEl.setAttribute("value", `${latitude}`);
			longitudeEl.setAttribute("value", `${longitude}`);
		});
	}
});
