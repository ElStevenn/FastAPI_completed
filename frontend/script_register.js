console.log("Hello world! This is register page!");



function post_user(email, username, password) {
    const newUsername = {
        email: email,
        username: username,
        password: password
    }

    fetch("http://127.0.0.1:8000/post_user", newUsername)
    .then(dat => {
        console.log("Message: ",dat);
    })
    .catch(err => {
        console.log("Error: ", err);
    });

}



// Key listener where where is what happends when the user clicks the "submit button"
document.getElementById("register_form").addEventListener('submit', (event) => {
    event.preventDefault(); // This avoid page reload (very important)

    let email = document.getElementById("email").value;
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username.length < 8) {
        document.getElementById("messages").textContent = "Your username must be at least 8 characters.";
        document.getElementById("messages").style = "Color: red;";
    } else if(password.length < 8) {
        document.getElementById("messages").textContent = "Your password must be at least 8 characters.";
        document.getElementById("messages").style = "Color: red;";
    }else{
        // Here execute the function to send the data to the post



        document.getElementById("messages").textContent = "You have been registered successfully!";
        document.getElementById("messages").style = "Color: green;";
    }


    console.log(email, username, password);

});


