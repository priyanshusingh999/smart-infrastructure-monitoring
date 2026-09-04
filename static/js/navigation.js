// // ==========================================
// // NAVIGATION
// // ==========================================

function initializeNavigation() {
    const navButtons = document.querySelectorAll(".nav-btn");

    navButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            // Active class remove from all buttons
            navButtons.forEach(function (btn) {
                btn.classList.remove("active");
            });

            // Current button active
            this.classList.add("active");

            // Flask URL stored in data-url
            const url = this.dataset.url;

            if (url) {
                window.location.href = url;
            }

        });

    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeNavigation);
} else {
    initializeNavigation();
}