// static/js/app.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("cvForm");
    const loader = document.getElementById("loader");

    if (form) {
        form.addEventListener("submit", () => {
            if (loader) loader.style.display = "block";
        });
    }
});
