const loginBtn = document.querySelector("#login-btn");
const backBtn = document.querySelector("#back-btn");
const aboutUsBtn = document.querySelector("#about-us-btn");
const container = document.querySelector(".container");

aboutUsBtn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

backBtn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

loginBtn.addEventListener("click", async (event) => {
  event.preventDefault(); // Prevent the default form submission

  const formData = new FormData(document.querySelector(".sign-in-form"));
  const username = formData.get("username");

  const password = formData.get("password");

  try {
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (data.statuscode==200) {
      // Successful login
      console.log("Login successful:", data);
      debugger
      const userid = data.userid
      const username = data.username
      localStorage.setItem('userid', userid);
      localStorage.setItem('username', username);
      // Redirect to the dashboard or perform other actions
      window.location.href = "/home.html";
    } else {
      // Failed login
      console.error("Login failed:", data.message);
      document.getElementById('errorMessage').innerText =data.message;
    }
  } catch (error) {
    console.error("Error during login:", error);
    alert("An unexpected error occurred. Please try again.");
  }
});
