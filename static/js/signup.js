document.addEventListener("DOMContentLoaded", function () {

    const passwordButtons =
        document.querySelectorAll(".show-password");


    passwordButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const targetId =
                this.getAttribute("data-target");

            const input =
                document.getElementById(targetId);


            if (!input) {
                return;
            }


            if (input.type === "password") {

                input.type = "text";

                this.textContent = "🙈";

            } else {

                input.type = "password";

                this.textContent = "👁";

            }

        });

    });


    // Password confirmation

    const form = document.querySelector("form");

    const password =
        document.getElementById("password");

    const confirmPassword =
        document.getElementById("confirm_password");


    if (form && password && confirmPassword) {

        form.addEventListener("submit", function (event) {

            if (password.value !== confirmPassword.value) {

                event.preventDefault();

                alert("Passwords do not match.");

                confirmPassword.focus();

            }

        });

    }

});