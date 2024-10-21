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
    // Load the value of the label by default
    confidenceRange.value = 60;
    labelSpan.textContent = `${confidenceRange.value}%`;
})

confidenceRange.addEventListener('input', e => {
    // Update label value with input value in real time
    labelSpan.textContent = `${confidenceRange.value}%`;
})

openConfig.addEventListener('click', () => {
    configSide.classList.remove('hide')
})

exitConfig.addEventListener('click', () => {
    configSide.classList.add('hide')
})

// Activar input (selector de imagenes) al hacer click en el div
dropZone.addEventListener('click', ()=> imageInput.click())

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drop-zone--active");
});

dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--active");
});

// Evento para cargar la imagen que se sube con drag-drop al input
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--active");
    // processedImage.src = "../../assets/backgroud.gif";
    // El archivo que se subio mediante drag-drop se colocara en los archivos del input (como si se subiera al input)
    processImage(e.dataTransfer.files[0]).then(res => {
        // console.log(res);
        processedImage.src = "data:image/png;base64," + res.image;
    });
    // console.log(inferedImage);
    // processedImage.src = processImage(e.dataTransfer.files[0])
    imageInput.files = e.dataTransfer.files
    // console.log(e.dataTransfer.files);
})

imageInput.addEventListener("change", () => {
    // console.log(imageInput.files);
    // processedImage.src = "data:image/png;base64" + processImage(imageInput.files[0])
    // processedImage.src = "../../assets/backgroud.gif";
    if (imageInput.files[0]){
        processImage(imageInput.files[0]).then((res) => {
            console.log(res);
            // setTitle(res.data);
            processedImage.src = "data:image/png;base64," + res.image;
        });
    }
    //COMENTARIO Esto lo vimos antes y nos devuelve lo mismo que en el caso anterior con el dataTransfer
    // Esto se dispara cuando el input cambie
});


// imageInput.addEventListener("change", () => {
    
// });

// const file = imageInput.files[0];
const processImage = async (image) => {
    if (!image) {
        // alert("Please, choose an image first.");
        showModal("Please, choose an image first.", false);
        return;
    }

    // Mostrar la imagen en la página web
    originalImage.src = URL.createObjectURL(image);
    processedImage.src = "../../assets/backgroud.gif";
    
    // const reader = new FileReader();
    // reader.onload = (e) => {
    //     originalImage.src = e.target.result;
    //     processedImage.src = "../../assets/backgroud.gif";

        // Procesar porporciones / tamaño
        // fheight = originalImage.clientHeight;
        // fwidth = originalImage.clientWidth;

        // processedImage
        // processedImage 
        // console.log(fheight);
        // console.log(fwidth);
    // };
    // reader.readAsDataURL(image);
    
    //* Obtener medidas de la imagen
    // originalImage.onload = () => {
    //     const iheight = originalImage.naturalHeight;
    //     const iwidth = originalImage.naturalWidth;
    //     console.log(iheight, iwidth);
    // };

    // const configData = {
    //     model: configForm.configModel.value,
    //     gpu: configForm.gpu.checked,
    //     confidence: Number(`0.${configForm.confidence.value}`),
    // };

    // Enviar la imagen al servidor
    const formData = new FormData();
    formData.append("image", image);
    // formData.append(
    //     "model",
    //     configForm.configModel.value === "custom"
    //         ? "dev/runs/detect/train8/weights/best.pt"
    //         : `${configForm.configModel.value}.pt`
    // );
    formData.append("model", configForm.configModel.value);
    // formData.append("gpu", configForm.gpu.checked);
    formData.append("confidence", `0.${configForm.confidence.value}`)

    try {
        const response = await fetch("http://localhost:5000/inference", {
        // const response = await fetch("https://fruit.homis.duckdns.org/api/inference", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (data.ok){
            showModal("Your image is ready", true);
        }else{
            // showModal("There was an issue while recovering data", false);
            showModal(`Error: ${data.details}`, false);
        }

        return data;
    } catch (err) {
        // console.error("Error:", err);
        showModal(`Error: ${err}`, false);
        // alert("There was an issue while recovering data.");
    }
        // .then((data) => {
            // console.log(data);
            // processedImage.src = "data:image/png;base64," + data.image;
            // return data.image;
            // document.body.appendChild(img);
        // })
        // .catch((error) => {
        //     console.error("Error:", error);
        //     alert("There was an issue while recovering data.");
        // });
}

const setTitle = (jsonData) => {
    jsonData = JSON.parse(jsonData)
    let frame = [];

    jsonData.forEach(element => {
        frame.push(element.name, element.confidence)
    });

    frame = frame.toString()
    console.log(frame);
}

const showModal = (msg, goodNews=false, timeOut=5000) => {
    modal.dataset.good = goodNews;
    modal.children[0].textContent = msg;
    setTimeout(() => {
        modal.dataset.good = "";
    }, timeOut);
}