const imageInput = document.getElementById("imageInput");
const originalImage = document.getElementById("originalImage");
const processedImage = document.getElementById("processedImage");
const dropZone = document.getElementById("dropZone");

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
    // El archivo que se subio mediante drag-drop se colocara en los archivos del input (como si se subiera al input)
    processImage(e.dataTransfer.files[0]).then(res => {
        // console.log(res);
        processedImage.src = "data:image/png;base64," + res;

    });
    // console.log(inferedImage);
    // processedImage.src = processImage(e.dataTransfer.files[0])
    imageInput.files = e.dataTransfer.files
    console.log(e.dataTransfer.files);
})

imageInput.addEventListener("change", () => {
    // console.log(imageInput.files);
    // processedImage.src = "data:image/png;base64" + processImage(imageInput.files[0])
    processImage(imageInput.files[0]).then((res) => {
        // console.log(res);
        processedImage.src = "data:image/png;base64," + res;
    });
    //COMENTARIO Esto lo vimos antes y nos devuelve lo mismo que en el caso anterior con el dataTransfer
    // Esto se dispara cuando el input cambie
});


// imageInput.addEventListener("change", () => {
    
// });

// const file = imageInput.files[0];
const processImage = async (image) => {
    if (!image) {
        alert("Please, choose an image first.");
        return false;
    }

    // Mostrar la imagen en la página web
    const reader = new FileReader();
    reader.onload = (e) => {
        originalImage.src = e.target.result;
    };
    reader.readAsDataURL(image);

    // Enviar la imagen al servidor
    const formData = new FormData();
    formData.append("image", image);

    try {
        const response = await fetch("http://localhost:5000/inference", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        return data.image;
    } catch (err) {
        console.error("Error:", err);
        alert("There was an issue while recovering data.");
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