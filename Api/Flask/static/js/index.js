const rangePriceInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
range = document.querySelector(".slider .progress");
let priceGap = 1000;

const rangeSpeedInput = document.querySelectorAll(".range-speed-input input"),
  speedInput = document.querySelectorAll(".speed-input input"),
  rangeSpeed = document.querySelector(".slider-speed .progress-speed"); // Change ".slider .progress" to ".slider-speed .progress-speed"
let SpeedGap = 1

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