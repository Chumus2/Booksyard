// For showing password
function toggle_password() {

    const password_input = document.getElementById("password");

    if (password_input.type == "password") {
        password_input.type = "text";
    }
    else {
        password_input.type = "password";
    };

};


// For Error 
setTimeout(function () {

    const error_message = document.getElementById("error_message")

    if (error_message) {
        error_message.style.display = "none"
    };

}, 3000);