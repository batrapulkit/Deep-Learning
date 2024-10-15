<script>
    // Handling form submission for Parking Prediction
    const parkingForm = document.getElementById('parking-form');
    parkingForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(parkingForm);
        const response = await fetch('/predict_parking', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        document.getElementById('result-parking').textContent = 'Parking Prediction: ' + JSON.stringify(result.prediction);
    });

    // Handling form submission for Image Label Prediction
    const imageForm = document.getElementById('image-form');
    imageForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(imageForm);
        const response = await fetch('/predict_image_label', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        document.getElementById('result-image').textContent = 'Image Label Prediction: ' + JSON.stringify(result.label);
    });
</script>