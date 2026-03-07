// For showing password
function toggle_password() {

    const password_input = document.getElementById("password1");

    if (password_input.type == "password") {
        password_input.type = "text";
    }
    else {
        password_input.type = "password";
    };

};