const rangePriceInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
range = document.querySelector(".slider .progress");
let priceGap = 1;

const rangeSpeedInput = document.querySelectorAll(".range-speed-input input"),
  speedInput = document.querySelectorAll(".speed-input input"),
  rangeSpeed = document.querySelector(".slider-speed .progress-speed"); // Change ".slider .progress" to ".slider-speed .progress-speed"
let SpeedGap = 1

// Variables pour les filtres Litres/100 km
const rangeL100Input = document.querySelectorAll(".range-l-100-input input");
const l100Input = document.querySelectorAll(".l-100-input input");
const rangeL100 = document.querySelector(".slider-l-100 .progress-l-100");
let l100Gap = 1;

// Variables pour les filtres Accélérations
const rangeAccelerationInput = document.querySelectorAll(".range-acceleration-input input");
const accelerationInput = document.querySelectorAll(".acceleration-input input");
const rangeAcceleration = document.querySelector(".slider-acceleration .progress-acceleration");
let accelerationGap = 1;

// Variables pour les filtres Puissances (CH)
const rangePowerInput = document.querySelectorAll(".range-power-input input");
const powerInput = document.querySelectorAll(".power-input input");
const rangePower = document.querySelector(".slider-power .progress-power");
let powerGap = 1;

priceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);

        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangePriceInput[1].max){
            if(e.target.className === "input-min"){
                rangePriceInput[0].value = minPrice;
                range.style.left = ((minPrice / rangePriceInput[0].max) * 100) + "%";
            }else{
                rangePriceInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangePriceInput[1].max) * 100 + "%";
            }
        }
    });
});

speedInput.forEach(input => {
    input.addEventListener("input", e => {
        let minSpeed = parseInt(speedInput[0].value),
            maxSpeed = parseInt(speedInput[1].value);

            if ((maxSpeed - minSpeed >= SpeedGap) && maxSpeed <= rangeSpeedInput[1].max) {
                if (e.target.className === "input-speed-min") { // Change "input-min" to "input-speed-min"
                    rangeSpeedInput[0].value = minSpeed;
                    rangeSpeed.style.left = ((minSpeed / rangeSpeedInput[0].max) * 100) + "%";
                } else {
                    rangeSpeedInput[1].value = maxSpeed;
                    rangeSpeed.style.right = 100 - (maxSpeed / rangeSpeedInput[1].max) * 100 + "%";
                }
            }
    });
});

// Écouteurs d'événements pour les filtres Litres/100 km
l100Input.forEach(input => {
    input.addEventListener("input", e => {
        let minL100 = parseInt(l100Input[0].value);
        let maxL100 = parseInt(l100Input[1].value);

        if ((maxL100 - minL100 >= l100Gap) && maxL100 <= rangeL100Input[1].max) {
            if (e.target.className === "input-l-100-min") {
                rangeL100Input[0].value = minL100;
                rangeL100.style.left = ((minL100 / rangeL100Input[0].max) * 100) + "%";
            } else {
                rangeL100Input[1].value = maxL100;
                rangeL100.style.right = 100 - (maxL100 / rangeL100Input[1].max) * 100 + "%";
            }
        }
    });
});

// Écouteurs d'événements pour les filtres Accélérations
accelerationInput.forEach(input => {
    input.addEventListener("input", e => {
        let minAcceleration = parseInt(accelerationInput[0].value);
        let maxAcceleration = parseInt(accelerationInput[1].value);

        if ((maxAcceleration - minAcceleration >= accelerationGap) && maxAcceleration <= rangeAccelerationInput[1].max) {
            if (e.target.className === "input-acceleration-min") {
                rangeAccelerationInput[0].value = minAcceleration;
                rangeAcceleration.style.left = ((minAcceleration / rangeAccelerationInput[0].max) * 100) + "%";
            } else {
                rangeAccelerationInput[1].value = maxAcceleration;
                rangeAcceleration.style.right = 100 - (maxAcceleration / rangeAccelerationInput[1].max) * 100 + "%";
            }
        }
    });
});

// Écouteurs d'événements pour les filtres Puissances (CH)
powerInput.forEach(input => {
    input.addEventListener("input", e => {
        let minPower = parseInt(powerInput[0].value);
        let maxPower = parseInt(powerInput[1].value);

        if ((maxPower - minPower >= powerGap) && maxPower <= rangePowerInput[1].max) {
            if (e.target.className === "input-power-min") {
                rangePowerInput[0].value = minPower;
                rangePower.style.left = ((minPower / rangePowerInput[0].max) * 100) + "%";
            } else {
                rangePowerInput[1].value = maxPower;
                rangePower.style.right = 100 - (maxPower / rangePowerInput[1].max) * 100 + "%";
            }
        }
    });
});

rangePowerInput.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangePowerInput[0].value);
        let maxVal = parseInt(rangePowerInput[1].value);
        if ((maxVal - minVal) < powerGap) {
            if (e.target.className === "range-power-min") {
                rangePowerInput[0].value = maxVal - powerGap;
            } else {
                rangePowerInput[1].value = minVal + powerGap;
            }
        } else {
            powerInput[0].value = minVal;
            powerInput[1].value = maxVal;
            rangePower.style.left = ((minVal / rangePowerInput[0].max) * 100) + "%";
            rangePower.style.right = 100 - (maxVal / rangePowerInput[1].max) * 100 + "%";
        }
    });
});

rangeAccelerationInput.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangeAccelerationInput[0].value);
        let maxVal = parseInt(rangeAccelerationInput[1].value);
        if ((maxVal - minVal) < accelerationGap) {
            if (e.target.className === "range-acceleration-min") {
                rangeAccelerationInput[0].value = maxVal - accelerationGap;
            } else {
                rangeAccelerationInput[1].value = minVal + accelerationGap;
            }
        } else {
            accelerationInput[0].value = minVal;
            accelerationInput[1].value = maxVal;
            rangeAcceleration.style.left = ((minVal / rangeAccelerationInput[0].max) * 100) + "%";
            rangeAcceleration.style.right = 100 - (maxVal / rangeAccelerationInput[1].max) * 100 + "%";
        }
    });
});

rangeL100Input.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangeL100Input[0].value);
        let maxVal = parseInt(rangeL100Input[1].value);
        if ((maxVal - minVal) < l100Gap) {
            if (e.target.className === "range-l-100-min") {
                rangeL100Input[0].value = maxVal - l100Gap;
            } else {
                rangeL100Input[1].value = minVal + l100Gap;
            }
        } else {
            l100Input[0].value = minVal;
            l100Input[1].value = maxVal;
            rangeL100.style.left = ((minVal / rangeL100Input[0].max) * 100) + "%";
            rangeL100.style.right = 100 - (maxVal / rangeL100Input[1].max) * 100 + "%";
        }
    });
});

rangePriceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minVal = parseInt(rangePriceInput[0].value),
        maxVal = parseInt(rangePriceInput[1].value);
        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
                rangePriceInput[0].value = maxVal - priceGap
            }else{
                rangePriceInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = ((minVal / rangePriceInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangePriceInput[1].max) * 100 + "%";
        }
    });
});

rangeSpeedInput.forEach(input => {
    input.addEventListener("input", e => {
        let minSpeed = parseInt(rangeSpeedInput[0].value),
            maxSpeed = parseInt(rangeSpeedInput[1].value);
        if ((maxSpeed - minSpeed) < SpeedGap) {
            if (e.target.className === "range-speed-min") {
                rangeSpeedInput[0].value = maxSpeed - SpeedGap;
            } else {
                rangeSpeedInput[1].value = minSpeed + SpeedGap;
            }
        } else {
          speedInput[0].value = minSpeed;
          speedInput[1].value = maxSpeed;
          rangeSpeed.style.left = ((minSpeed / rangeSpeedInput[0].max) * 100) + "%";
          rangeSpeed.style.right = 100 - (maxSpeed / rangeSpeedInput[1].max) * 100 + "%";
        }
    });
});

const min_speed = document.getElementsByName('speed-min')
const max_speed = document.getElementsByName('speed-max')
const min_l_100 = document.getElementsByName('l-100-min')
const max_l_100 = document.getElementsByName('l-100-max')
const min_power = document.getElementsByName('power-min')
const max_power = document.getElementsByName('power-max')
const min_acc = document.getElementsByName('acc-min')
const max_acc = document.getElementsByName('acc-max')

document.addEventListener("DOMContentLoaded", function () {
    const priceMinInput = document.getElementById("price-min");
    const priceMaxInput = document.getElementById("price-max");

    const initialMinPrice = parseInt(priceMinInput.value);
    const initialMaxPrice = parseInt(priceMaxInput.value);
});
