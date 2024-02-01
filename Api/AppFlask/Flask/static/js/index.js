// Get the HTML element with the id 'allForme'
const allForme = document.getElementById('allForme');

// Define an array of form element IDs
const formElements = [
    'price-min', 'price-max',
    'l-100-min', 'l-100-max',
    'speed-min', 'speed-max',
    'power-min', 'power-max',
    'accel-min', 'accel-max'
];

// Iterate through the form element IDs using forEach
formElements.forEach(elementId => {
    // Get the HTML element with the current elementId
    const element = document.getElementById(elementId);

    // Add an event listener for the 'change' event on the element
    element.addEventListener('change', () => {
        // When the element's value changes, submit the 'allForme' form
        allForme.submit();
    });
});

