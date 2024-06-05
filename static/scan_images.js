window.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(function(img) {
        const imageId = img.id.split('-')[1];
        const scanResultElement = document.getElementById(`scan-result-${imageId}`);

        fetch('/scan_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image_url: img.src })
        })
        .then(response => response.json())
        .then(data => {
            scanResultElement.textContent = data.result;
        })
        .catch(error => {
            scanResultElement.textContent = 'Error scanning image';
            console.error('Error scanning image:', error);
        });
    });
});