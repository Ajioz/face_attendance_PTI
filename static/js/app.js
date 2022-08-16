const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");

const login = document.getElementById("login");
const register = document.getElementById("register");

const container = document.getElementById("container");

signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});

register.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

login.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});