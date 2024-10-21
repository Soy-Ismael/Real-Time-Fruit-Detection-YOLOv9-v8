const imageInput = document.getElementById("imageInput");
const originalImage = document.getElementById("originalImage");
const processedImage = document.getElementById("processedImage");
const dropZone = document.getElementById("dropZone");
const configForm = document.getElementById("configForm");

const openConfig = document.getElementById("configButton");
const exitConfig = document.getElementById("exitConfigButton");
const confidenceRange = document.getElementById("configConfidence");
const labelSpan = document.getElementById("configConfidenceValue");
const configSide = document.getElementById("configSide");

const modal = document.getElementById('modal');


addEventListener('DOMContentLoaded', () => {
    confidenceRange.value = 60;
    labelSpan.textContent = `${confidenceRange.value}%`;
})

confidenceRange.addEventListener('input', e => {
    labelSpan.textContent = `${confidenceRange.value}%`;
})

openConfig.addEventListener('click', () => {
    configSide.classList.remove('hide')
})

exitConfig.addEventListener('click', () => {
    configSide.classList.add('hide')
})

dropZone.addEventListener('click', ()=> imageInput.click())

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drop-zone--active");
});

dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--active");
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--active");
    processImage(e.dataTransfer.files[0]).then(res => {
        processedImage.src = "data:image/png;base64," + res.image;
    });
    imageInput.files = e.dataTransfer.files
})

imageInput.addEventListener("change", () => {
    if (imageInput.files[0]){
        processImage(imageInput.files[0]).then((res) => {
            processedImage.src = "data:image/png;base64," + res.image;
        });
    }
});

const processImage = async (image) => {
    if (!image) {
        showModal("Please, choose an image first.", false);
        return;
    }

    originalImage.src = URL.createObjectURL(image);
    processedImage.src = "../../assets/backgroud.gif";

    const formData = new FormData();
    formData.append("image", image);
    formData.append("model", configForm.configModel.value);
    formData.append("gpu", configForm.gpu.checked);
    formData.append("confidence", `0.${configForm.confidence.value}`);

    try {
        const response = await fetch("http://localhost:5000/inference", {
            // const response = await fetch("https://fruit.homis.duckdns.org/api/inference", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (data.ok) {
            showModal("Your image is ready", true);
        } else {
            showModal(`Error: ${data.details}`, false);
        }

        return data;
    } catch (err) {
        showModal(`Error: ${err}`, false);
    }
}

const showModal = (msg, goodNews=false, timeOut=5000) => {
    modal.dataset.good = goodNews;
    modal.children[0].textContent = msg;
    setTimeout(() => {
        modal.dataset.good = "";
    }, timeOut);
}