// let authSocialFacebook = document.querySelector(".social-facebook ");
//
// authSocialFacebook.addEventListener("click", (event) => {
//     let request = new XMLHttpRequest();
//     request.open("GET", "http://localhost:8000/auth/sign/facebook");
//     request.setRequestHeader("content-type", "application/json");
//     request.addEventListener("load", (event) => {
//         let response = request.responseText;
//
//         let data = JSON.parse(response);
//         console.log(data);
//     });
//     request.send();
// });