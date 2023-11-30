"use strict";

const passwordInput = document.querySelector(".password-input--box input");
// const eyeIcon = document.querySelector(".password-input--box i");
const requirementsListEl = document.querySelectorAll(".requirement-list li");

// console.log(parent)
console.log(requirementsListEl)
console.log(passwordInput)
console.log("Hello Test")
const requirements = [
    { regex: /.{8,20}$/, index: 0 },
    { regex: /[0-9]/, index: 1 },
    { regex: /[a-z]/, index: 2 },
    { regex: /[#?!@$%^&*\-_]+/, index: 3 },
    { regex: /[A-Z]/, index: 4 },
];

passwordInput.addEventListener("keyup", (e) => {
    requirements.forEach((item) => {
        const isValid = item.regex.test(e.target.value);
        const requirementItem = requirementsListEl[item.index];

        if (isValid) {
            console.log(requirementItem);
            requirementItem.firstElementChild.className = "fa-solid fa-check";
            requirementItem.classList.add("valid");
        } else {
            requirementItem.firstElementChild.className = "fa-solid fa-circle";
            requirementItem.classList.remove("valid");
        }
    });
});

// eyeIcon.addEventListener("click", function () {
// 	passwordInput.type =
// 		passwordInput.type === "password" ? "text" : "password";

// 	eyeIcon.className = `fa-solid fa-eye${
// 		passwordInput.type === "password" ? "" : "-slash"
// 	}`;
// });