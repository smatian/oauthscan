document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        const imgId = img.id.split('-')[1]; // Extract ID from the img element
        fetch('/scan_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image_url: img.src })
        })
        .then(response => response.json())
        .then(data => {
            const resultElement = document.getElementById(`result-${imgId}`);
            resultElement.innerHTML = `Scan result: ${data.result}`;
        })
        .catch(error => {
            const resultElement = document.getElementById(`result-${imgId}`);
            resultElement.innerHTML = `Error scanning image: ${error}`;
        });
    });
});
