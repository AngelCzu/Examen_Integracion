 carrito = JSON.parse(localStorage.getItem("carrito")) || [];

 body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      product = body.querySelector("#dropdown"),
      logout = body.querySelector("#logout"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = document.querySelector(".mode-text");

// Oculta el icono del sol por defecto
document.getElementById("icon_sol").style.display = "none";

// Función para activar el modo oscuro
function activateDarkMode() {
    body.classList.add("dark");
    document.getElementById("icon_luna").style.display = "none";
    document.getElementById("icon_sol").style.display = "inline";
    modeText.innerText = "Light mode";
}

// Función para desactivar el modo oscuro
function deactivateDarkMode() {
    body.classList.remove("dark");
    document.getElementById("icon_luna").style.display = "inline";
    document.getElementById("icon_sol").style.display = "none";
    modeText.innerText = "Dark mode";
}

// Verifica si el modo oscuro está habilitado en el almacenamiento local
const isDarkModeEnabled = JSON.parse(localStorage.getItem("darkModeEnabled"));

// Si el modo oscuro está habilitado, actívalo
if (isDarkModeEnabled) {
    activateDarkMode();
}

// Listener para el botón de modo oscuro
modeSwitch.addEventListener("click", () => {
    // Toggle del modo oscuro
    body.classList.toggle("dark");
    const isDarkModeEnabled = body.classList.contains("dark");

    // Actualiza el estado en el almacenamiento local
    localStorage.setItem("darkModeEnabled", isDarkModeEnabled);

    // Actualiza la interfaz de acuerdo al modo
    if (isDarkModeEnabled) {
        activateDarkMode();
    } else {
        deactivateDarkMode();
    }
});

// Listeners para eventos en la barra lateral
toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

searchBtn.addEventListener("click", () => {
    sidebar.classList.remove("close");
});

product.addEventListener("click", () => {
    sidebar.classList.remove("close");
});

logout.addEventListener("click", () => {
    sidebar.classList.remove("close");
});

