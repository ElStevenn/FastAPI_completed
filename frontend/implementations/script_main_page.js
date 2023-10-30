console.log("Checking out if this works!");

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