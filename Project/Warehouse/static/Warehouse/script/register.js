"use strict";

const latitudeEl = document.getElementById("latitude");
const longitudeEl = document.getElementById("longitude");

const detectButton = document.querySelector(".button-8");

detectButton.addEventListener("click", function() {
    if (navigator.geolocation) {
        const options = {
            enableHighAccuracy: true,
            timeout: 500, // Timeout in milliseconds (adjust as needed)
            maximumAge: 0 // Maximum age of a cached position (force refresh)
        };
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                // latitudeEl.setAttribute("value", `${latitude}`);
                // longitudeEl.setAttribute("value", `${longitude}`);
                latitudeEl.value = parseFloat(latitude.toFixed(9)); // Adjust the precision as needed
                longitudeEl.value = parseFloat(longitude.toFixed(9)); // Adjust the precision as needed
                console.log(latitudeEl.value)
                console.log(longitudeEl.value)
            },
            (error) => {
                console.error(`Error getting location: ${error.message}`);
            },
            options
        );
    }
});