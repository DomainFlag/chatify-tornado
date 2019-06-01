let author = document.querySelector(".message-header");
let authorName = document.querySelector(".message-author");

author.addEventListener("mouseover", (event) => {
    let request = new XMLHttpRequest();

    request.open("GET", "http://localhost:8000/user");
    request.addEventListener("load", (event) => {
        let user = JSON.parse(request.response);

        if(user.hasOwnProperty("name")) {
            authorName.style.display = "flex";

            authorName.innerHTML = user.name;
        }
    });

    request.send();
});