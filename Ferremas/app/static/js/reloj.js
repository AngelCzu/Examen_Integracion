const hora = document.getElementById('hora');
const AMPM = document.getElementById('AMPM')
const fecha = document.getElementById('fecha');
const diasSemana = [
  "Lunes", "Martes", "Miercoles", "Jueves", "Viernes","Sabado","Domingo",
]
const meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "September", "Octubre", "Noviembre", 
    "Diciembre"
];

const reloj = setInterval(() => {

    const local = new Date();
    
    let dia = local.getDate(),
        diaSemana = local.getDay(),
        mes = local.getMonth(),
        anio = local.getFullYear(),
        horas = local.getHours(),
        ampm = local.getHours();


        /*Formato para AM o PM*/
        if (horas >= 12) {
            horas = horas - 12;
            ampm = 'PM';
        }else{
            ampm = 'AM';
        }

        hora.innerHTML = local.toLocaleTimeString() + ` ${ampm}`;
        fecha.innerHTML = `${diasSemana[diaSemana]}, ${dia} de ${meses[mes]}  de ${anio}`;

}, 1);