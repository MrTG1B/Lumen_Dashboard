const form = document.getElementById("login-form");
const name = document.getElementById("name");
const password = document.getElementById("password");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // Check if any field is empty
    if (name.value === "" || password.value === "") {
        alert("Please fill all the fields");
    }
    else {
        // Check if the username is 'Tirtha' and password is '12345678'
        if (name.value === "Tirtha" && password.value === "12345678") {
            // Redirect to the next page
            window.location.href = "dashboard/dashboard.html";
        } else {
            alert("Invalid username or password");
        }
    }
});
