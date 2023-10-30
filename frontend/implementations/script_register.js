console.log("Hello world! This is register page!");



async function post_user(email, username, password) {
    // Call API to post a new user. | Async function because an API call is needed (https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
    const newUsername = {
        email: email,
        username: username,
        password: password,
        is_active: false
    }

    try{
        const response = await fetch("http://127.0.0.1:8000/post_user", {
            "method": "POST",
            "mode": "cors",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(newUsername),

        });

        const result = await response.json();
        console.log("Response: ", result)

    } catch(error) {
        console.log("Error: ", error)
    }
    
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


        post_user(email, username, password);
        document.getElementById("messages").textContent = "You have been registered successfully!";
        document.getElementById("messages").style = "Color: green;";
        window.location.href = "http://127.0.0.1:5500/PostgreSQL/LoginPasword/frontend/entry_page.html";

    }


    console.log(email, username, password);

});


