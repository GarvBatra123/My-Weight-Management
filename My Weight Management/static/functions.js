// ----------------------------------------------------------------------------------------------------------------------------
// THIS FUNCTION IS FOR "createAcc-Pg1_formatting"
// TO TOGGLE PASSWORD VISIBILITY
// REFERENCE LINK: https://www.youtube.com/watch?v=iA9ZxELnikM

var passwordField = document.querySelector('.userPW'); //obtain data in password input box and store it
var show = document.querySelector('.show'); //obtain icon in "fa class" type "fa-eye" -> click to show pw
var hide = document.querySelector('.hide'); //obtain icon in "fa class" type "fa-eye-slash" -> click to hide pw

show.onclick = function () { //define function to be called when user wants to see pw
    passwordField.setAttribute("type", "text"); //convert input type "password" to type "text"
    show.style.display = "none"; //remove the icon in "fa class" type "fa-eye"
    hide.style.display = "inline-block";
}

hide.onclick = function () { //define function to be called when user wants to hide pw
    passwordField.setAttribute("type", "password"); //reverse the process done in "show.onclick=function"
    hide.style.display = "none"; //remove the icon in "fa class" type "fa-eye-slash"
    show.style.display = "inline-block"
}
// ----------------------------------------------------------------------------------------------------------------------------
