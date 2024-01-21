const allForme = document.getElementById('allForme');
const formElements = [
    'price-min', 'price-max',
    'l-100-min', 'l-100-max',
    'speed-min', 'speed-max',
    'power-min', 'power-max',
    'accel-min', 'accel-max'
];

formElements.forEach(elementId => {
    const element = document.getElementById(elementId);
    element.addEventListener('change', () => {
        allForme.submit();
    });
});
