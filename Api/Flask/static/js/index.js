// Fonction pour update les ranges et les inputs des filtres
function updateFilterInput(filterInput, rangeInput, range, gap) {
    filterInput.forEach(input => {
        input.addEventListener("input", e => {
            let minValue = parseInt(filterInput[0].value);
            let maxValue = parseInt(filterInput[1].value);

            if ((maxValue - minValue >= gap) && maxValue <= rangeInput[1].max) {
                rangeInput[0].value = minValue;
                rangeInput[1].value = maxValue;
                range.style.left = `${(minValue / rangeInput[0].max) * 100}%`;
                range.style.right = `${100 - (maxValue / rangeInput[1].max) * 100}%`;
            }
        });
    });
}

// Variables pour les filtres Prix (€)
const rangePriceInput = document.querySelectorAll(".range-price input");
const priceInput = document.querySelectorAll(".price-input input");
const rangePrice = document.querySelector(".slider .progress-price");
let priceGap = 1000;

updateFilterInput(priceInput, rangePriceInput, rangePrice, priceGap)

rangePriceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minVal = parseInt(rangePriceInput[0].value),
        maxVal = parseInt(rangePriceInput[1].value);
        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-price-min"){
                rangePriceInput[0].value = maxVal - priceGap
            }else{
                rangePriceInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            rangePrice.style.left = ((minVal / rangePriceInput[0].max) * 100) + "%";
            rangePrice.style.right = 100 - (maxVal / rangePriceInput[1].max) * 100 + "%";
        }
    });
});

// Variables pour les filtres Vitesse (km/h)
const rangeSpeedInput = document.querySelectorAll(".range-speed input");
const speedInput = document.querySelectorAll(".speed-input input");
const rangeSpeed = document.querySelector(".slider .progress-speed");
let SpeedGap = 1

updateFilterInput(speedInput, rangeSpeedInput, rangeSpeed, SpeedGap)

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

// Variables pour les filtres Litres/100 km
const rangeL100Input = document.querySelectorAll(".range-l-100 input");
const l100Input = document.querySelectorAll(".l-100-input input");
const rangeL100 = document.querySelector(".slider .progress-l-100");
let l100Gap = 1;

updateFilterInput(l100Input, rangeL100Input, rangeL100, l100Gap)

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

// Variables pour les filtres Puissance (CH)
const rangePowerInput = document.querySelectorAll(".range-power input");
const powerInput = document.querySelectorAll(".power-input input");
const rangePower = document.querySelector(".slider .progress-power");
let powerGap = 1;

updateFilterInput(powerInput, rangePowerInput, rangePower, powerGap)

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

// Variables pour les filtres Accélération
const rangeAccelerationInput = document.querySelectorAll(".range-acceleration input");
const accelerationInput = document.querySelectorAll(".acceleration-input input");
const rangeAcceleration = document.querySelector(".slider .progress-acceleration");
let accelerationGap = 1;

updateFilterInput(accelerationInput, rangeAccelerationInput, rangeAcceleration, accelerationGap)

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

// Collecte le Forme
const allForme = document.getElementById('allForme');

// Collecte les valeurs des filtres des prix
const minPriceSelect = document.getElementById('price-min-range');
const maxPriceSelect = document.getElementById('price-max-range');

// Collecte les valeurs des filtres des L/100
const minL100Select = document.getElementById('l-100-min-range');
const maxL100Select = document.getElementById('l-100-max-range');

// Collecte les valeurs des filtres des vitesses
const minSpeedSelect = document.getElementById('speed-min-range');
const maxSpeedSelect = document.getElementById('speed-max-range');

// Collecte les valeurs des filtres des puissances
const minPowerSelect = document.getElementById('power-min-range');
const maxPowerSelect = document.getElementById('power-max-range');

// Collecte les valeurs des filtres des accélérations
const minAcccelSelect = document.getElementById('accel-min-range');
const maxAccelSelect = document.getElementById('accel-max-range');

minPriceSelect.addEventListener('change', () => {
    allForme.submit();
});

maxPriceSelect.addEventListener('change', () => {
    allForme.submit();
});

minSpeedSelect.addEventListener('change', () => {
    allForme.submit();
});

maxSpeedSelect.addEventListener('change', () => {
    allForme.submit();
});

minL100Select.addEventListener('change', () => {
    allForme.submit();
});

maxL100Select.addEventListener('change', () => {
    allForme.submit();
});

minPowerSelect.addEventListener('change', () => {
    allForme.submit();
});

maxPowerSelect.addEventListener('change', () => {
    allForme.submit();
});

minAcccelSelect.addEventListener('change', () => {
    allForme.submit();
});

maxAccelSelect.addEventListener('change', () => {
    allForme.submit();
});
