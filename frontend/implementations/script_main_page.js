console.log("Checking out if this works!");


// Get Session ID, in 
document.addEventListener("DOMContentLoaded", () => {
    checkSession();
  });
  
  async function checkSession() {
    try {
      const response = await fetch("http://localhost:8000/whoami", {
        credentials: "include",  // Required to send cookies
      });
  
      if (!response.ok) {
        throw new Error("Session not found");
      }
  
      const data = await response.json();
      document.getElementById("content").innerText = `Hello, ${data.user.username}!`;
    } catch (error) {
      console.error("Session check failed:", error);
      window.location.href = "http://127.0.0.1:5500/PostgreSQL/LoginPasword/frontend/login.html";
    }
  }
  

const an_owner_id = "3d6913a7-f1f5-4ffb-b26b-73e225530b9b";

async function get_books(owner_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/get_books_by_owner_id/${owner_id}`);
        console.log("Response Status:", response.status);
        return await response.json();
    } catch (error) {
        console.error("Error fetching books:", error);
        return "An error occurred";
    }
}

console.log(get_books(an_owner_id))