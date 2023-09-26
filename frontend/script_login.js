console.log("This is login page!");



async function Check_if_user(user, password) {
    const User_pass = {
        "username":user,
        "password":password
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/check_user", {
            "method":"POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(User_pass),

        });

        const result = await response.json();
        return result;

    } catch(error) {
        return error;
    }


}

let username = "MyOwnEmail@gmail.com";
let password = "ILikeButtifarrachange_this123";
(async () => {
    let result = await Check_if_user(username, password);
    console.log(result);
})();

// Since Check_if_user is an async function, it returns a Promise

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("login_form").addEventListener('submit', async (event) => {
        event.preventDefault();

        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        // Await the result first before accessing the 'result' attribute
        let checkResult = await Check_if_user(username, password);
        if (checkResult['result']) {
            document.getElementById("additional_text").textContent = `Logged successfully as ${username}`;
            document.getElementById("additional_text").style.color = "green";
            console.log(`Username ${username} exists!`)
        } else {
            document.getElementById("additional_text").textContent = `User ${username} doesn't exist!`;
            document.getElementById("additional_text").style.color = "red";
        }

        console.log(username, password);
    });
});
