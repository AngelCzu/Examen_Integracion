function consumApi(){

    /* Esto se utiliza para llamar a la api publica */
    fetch("https://api.openweathermap.org/data/2.5/weather?lat=-33.45694&lon=-70.64827&lang=es&appid=e7583f9125c2a26e1db48919d23bfc61")
    .then(response => response.json())
    .then(info => {
        
        let name = document.getElementById("resultDolar");
        let name2 = document.getElementById("resultDolar2");
        let name3 = document.getElementById("resultDolar3");
        let name4 = document.getElementById("resultDolar4");
        let name5 = document.getElementById("resultDolar5");
        let name6 = document.getElementById("resultDolar6");
        let name7 = document.getElementById("resultDolar7");
        
        

        /* Se le está insertando al h1 el valor del dolar y la información del clima */
        name.innerHTML += info.weather[0].main;
        name2.innerHTML += "<img src='https://openweathermap.org/img/wn/"+info.weather[0].icon+".png'>" + info.weather[0].description;
        name3.innerHTML +=  (info.main.temp - 273.15).toFixed(1) + " °C";
        name4.innerHTML += "Temperatura Fahrenheit: " + ((info.main.temp * 9/5) - 459.67).toFixed(1) + " °F";
        name5.innerHTML += "Temperatura Minima: " + (info.main.temp_min - 273.15).toFixed(1) + " °C";
        name6.innerHTML += "Temperatura Maxima: " + (info.main.temp_max - 273.15).toFixed(1) + " °C";
        name7.innerHTML += "Humedad: " + (info.main.humidity) + "%";
     })
    /* Esto se utiliza para resibir la informacion para transformarla en un formato .json */
    //.then(response => response.json())
}

consumApi();

//"Weather id: " + (info.main.temp - 273.15).toFixed(1) + " °C";
//"Weather id: " + ((info.main.temp * 9/5) - 459.67).toFixed(1) + " °F";