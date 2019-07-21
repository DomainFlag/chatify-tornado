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

let formElements = document.getElementsByClassName("form-element");
for(let g = 0; g < formElements.length; g++) {
    let formElement = formElements[g];

    let inputFormElement = formElement.querySelector(".element-input");
    let labelFormElement = formElement.querySelector(".auth-placeholder");

    inputFormElement.addEventListener("focus", (event) => {
        labelFormElement.classList.replace("auth-placeholder-idle", "auth-placeholder-active");
    });

    inputFormElement.addEventListener("blur", (event) => {
        if(inputFormElement.value == null || inputFormElement.value.length === 0) {
            labelFormElement.classList.replace("auth-placeholder-active", "auth-placeholder-idle");
        }
    });
}