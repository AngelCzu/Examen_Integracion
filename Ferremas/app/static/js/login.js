// PASSWORD EN REGISTRO
document.getElementById("ocultarReg").style.display = "none";

function passwordRegistro() {
    const mostrar = document.getElementById("mostrarReg");
    const input = document.getElementById("txtPasswordReg");
    if (input.type == "password") {
        input.type = "text";
        ocultarReg.style.display = "inline";
        mostrarReg.style.display = "none";
    } else {
        input.type = "password";
        ocultarReg.style.display = "none";
        mostrarReg.style.display = "inline";
    }
}

// PASSWORD EN INGRESAR
document.getElementById("ocultarIng").style.display = "none";
function passwordIngresar() {
    const mostrar = document.getElementById("mostrarIng");
    const input = document.getElementById("txtPasswordIng");
    if (input.type == "password") {
        input.type = "text";
        ocultarIng.style.display = "inline";
        mostrarIng.style.display = "none";
    } else {
        input.type = "password";
        ocultarIng.style.display = "none";
        mostrarIng.style.display = "inline";
    }
}

// FUNCIONES DEL DARKMODE

const toggle = document.getElementById('toggleDark'); // LISTO
const body = document.querySelector('body'); // LISTO
const contenedorP = document.getElementById('contenedorPrincipalBody'); // LISTO

// REGISTRO
const txtLabelReg = document.getElementById('txtLabelReg'); // LISTO
const labelTxtNomUsu = document.getElementById('labelTxtNomUsu'); // LISTO
const labelTxtCorreo = document.getElementById('labelTxtCorreo'); // LISTO
const labelTxtPassReg = document.getElementById('labelTxtPassReg'); // LISTO
const buttonTxtReg = document.getElementById('buttonTxtReg'); // LISTO
const houseIcon = document.getElementById('houseIcon'); // LISTO

// NUEVOS CAMPOS
const labelTxtApeUsu = document.getElementById('labelTxtApeUsu');
const labelTxtDirecReg = document.getElementById('labelTxtDirecReg');
const labelTxtNumReg = document.getElementById('labelTxtNumReg');

// INGRESAR
const contenedorIng = document.getElementById('contenedorIng'); // LISTO
const txtLabelIng = document.getElementById('txtLabelIng'); // LISTO
const labelTxtUsuIng = document.getElementById('labelTxtUsuIng'); // LISTO
const labelTxtPassIng = document.getElementById('labelTxtPassIng'); // LISTO
const buttonTxtIng = document.getElementById('buttonTxtIng'); // LISTO

toggle.addEventListener('click', function() {
    this.classList.toggle('bi-moon-stars-fill');
    if (this.classList.toggle('bi-brightness-high-fill')) {
        body.style.background = 'white';
        body.style.color = 'black';
        body.style.transition = '1s';

        contenedorP.style.background = 'white';
        contenedorP.style.color = 'black';
        contenedorP.style.transition = '1s';

        contenedorIng.style.background = '#f3f2f2';

        txtLabelIng.style.color = 'black';
        txtLabelReg.style.color = 'black';
        houseIcon.style.color = 'black';
        houseIcon.style.transition = '4.7s';

        labelTxtNomUsu.style.color = 'black';
        labelTxtCorreo.style.color = 'black';
        labelTxtPassReg.style.color = 'black';
        buttonTxtReg.style.color = 'white';

        labelTxtUsuIng.style.color = 'black';
        labelTxtPassIng.style.color = 'black';
        buttonTxtIng.style.color = 'white';

        // Nuevos campos
        labelTxtApeUsu.style.color = 'black';
        labelTxtDirecReg.style.color = 'black';
        labelTxtNumReg.style.color = 'black';
    } else {
        body.style.background = '#1E1E1E';
        body.style.color = 'white';
        body.style.transition = '1s';

        contenedorP.style.background = '#2d2d2d';
        contenedorP.style.color = 'white';
        contenedorP.style.transition = '1s';

        contenedorIng.style.background = '#454545';

        txtLabelIng.style.color = 'white';
        txtLabelReg.style.color = 'white';
        houseIcon.style.color = 'white';
        houseIcon.style.transition = '4.7s';

        labelTxtNomUsu.style.color = 'white';
        labelTxtCorreo.style.color = 'white';
        labelTxtPassReg.style.color = 'white';
        buttonTxtReg.style.color = 'white';

        labelTxtUsuIng.style.color = 'white';
        labelTxtPassIng.style.color = 'white';
        buttonTxtIng.style.color = 'white';

        // Nuevos campos
        labelTxtApeUsu.style.color = 'white';
        labelTxtDirecReg.style.color = 'white';
        labelTxtNumReg.style.color = 'white';
    }
});

// Selección de inputs al hacer clic en el label
labelTxtNomUsu.addEventListener('click', function() {
    document.getElementById('txtNomUsuReg').focus();
});
labelTxtApeUsu.addEventListener('click', function() {
    document.getElementById('txtApeUsuReg').focus();
});
labelTxtCorreo.addEventListener('click', function() {
    document.getElementById('txtCorreoReg').focus();
});
labelTxtDirecReg.addEventListener('click', function() {
    document.getElementById('txtDirecReg').focus();
});
labelTxtNumReg.addEventListener('click', function() {
    document.getElementById('txtNumReg').focus();
});

$(function() {
    $("#formReg").validate({
        rules: {
            txtNomUsuReg: {
                required: true,
                maxlength: 10
            },
            txtApeUsuReg: {
                required: true,
                maxlength: 20
            },
            txtCorreoReg: {
                required: true,
                email: true
            },
            txtDirecReg: {
                required: true
            },
            txtNumReg: {
                required: true,
                digits: true,
                minlength: 9,
                maxlength: 15
            },
            txtPasswordReg: {
                required: true
            },
            txtUsuIng: {
                required: true
            },
            txtPasswordIng: {
                required: true
            }
        },
        messages: {
            txtNomUsuReg: {
                required: "El nombre de usuario es un campo obligatorio",
                maxlength: "El máximo de caracteres es 10"
            },
            txtApeUsuReg: {
                required: "El apellido es un campo obligatorio",
                maxlength: "El máximo de caracteres es 20"
            },
            txtCorreoReg: {
                required: "El correo es un campo obligatorio",
                email: "El formato de correo no es válido"
            },
            txtDirecReg: {
                required: "La dirección es un campo obligatorio"
            },
            txtNumReg: {
                required: "El número de teléfono es un campo obligatorio",
                digits: "El número de teléfono debe contener solo dígitos",
                minlength: "El número de teléfono debe tener al menos 10 dígitos",
                maxlength: "El número de teléfono debe tener como máximo 15 dígitos"
            },
            txtPasswordReg: {
                required: "La contraseña es obligatoria"
            },
            txtUsuIng: {
                required: "El nombre de usuario es un campo obligatorio"
            },
            txtPasswordIng: {
                required: "La contraseña es un campo obligatorio"
            }
        }
    });
});

$(function() {
    $("#formLogin").validate({
        rules: {
            txtUsuIng: {
                required: true
            },
            txtPasswordIng: {
                required: true
            }
        },
        messages: {
            txtUsuIng: {
                required: "El nombre de usuario es un campo obligatorio"
            },
            txtPasswordIng: {
                required: "La contraseña es un campo obligatorio"
            }
        }
    });
});
