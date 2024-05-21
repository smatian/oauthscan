document.addEventListener("DOMContentLoaded", function() {
    const imageElements = document.querySelectorAll("img");
    let delay = 300;

    imageElements.forEach((img, index) => {
        setTimeout(() => {
            const imageUrl = img.src;
            const scanResultElement = img.nextElementSibling;

            fetch('/scan_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_url: imageUrl })
            })
            .then(response => response.json())
            .then(data => {
                scanResultElement.innerText = data.result;
            })
            .catch(error => {
                console.error('Error scanning image:', error);
                scanResultElement.innerText = 'Error scanning image';
            });
        }, index * delay);
    });
});
