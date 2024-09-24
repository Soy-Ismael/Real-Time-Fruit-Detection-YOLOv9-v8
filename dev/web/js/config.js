const configForm = document.getElementById("configForm");
const openConfig = document.getElementById("configButton");
const exitConfig = document.getElementById("exitConfigButton");
const confidenceRange = document.getElementById("configConfidence");
const labelSpan = document.getElementById("configConfidenceValue");
const configSide = document.getElementById("configSide");

addEventListener('DOMContentLoaded', () => {
    confidenceRange.value = 60;
    labelSpan.textContent = `${confidenceRange.value}%`;
})

confidenceRange.addEventListener('input', e => {
    labelSpan.textContent = `${confidenceRange.value}%`;
})

configForm.addEventListener('submit', e => {
    e.preventDefault();

    const path = location.href.endsWith("/")
        ? `${location.href}php/main.php`
        : location.href
              .replace("index.html", "php/main.php")
              .replace("index", "php/main.php");

    fetch(path, {
        method: 'POST',
        body: JSON.stringify({
            model : configForm.configModel.value,
            gpu : configForm.gpu.checked,
            confidence : Number(`0.${configForm.confidence.value}`),
        })
    })
    .then((res) => res.json())
    // .then(data => console.log(data))
    .catch((err) => {
        console.log(err);
    });

    configSide.classList.add('hide')
})

openConfig.addEventListener('click', () => {
    configSide.classList.remove('hide')
})

exitConfig.addEventListener('click', () => {
    configSide.classList.add('hide')
})