document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];  // Get the uploaded file
    const loader = document.getElementById('loader');  // Loader element
    const imagePreview = document.getElementById('imagePreview');  // Image preview container
    const submitButton = document.getElementById('submitButton');  // Submit button for image preview
    const saveButton = document.getElementById('saveButton');  // Save button to upload image to server

    if (file) {
        loader.style.display = 'block';  // Show the loader while processing
        imagePreview.style.display = 'none';  // Hide the image preview initially
        submitButton.style.display = 'none';  // Hide the submit button while loading
        saveButton.style.display = 'none';  // Hide the save button during loading

        const imageUrl = URL.createObjectURL(file);  // Create a URL for the image
        console.log("imageUrl=" + imageUrl);  // Log the image URL (for debugging)

        // Show the preview after a simulated loading time
        setTimeout(() => {
            loader.style.display = 'none';  // Hide loader after processing
            imagePreview.innerHTML = `<img src="${imageUrl}" alt="Uploaded Image" style="max-width: 100%; max-height: 100vh; display: block; margin: auto;">`;  // Display image
            imagePreview.style.display = 'block';  // Show the image preview
            submitButton.style.display = 'block';  // Show submit button
            saveButton.style.display = 'block';  // Show save button
        }, 3000);  // Simulate a 3-second loading time

        // Open the image in a new tab when the submit button is clicked
        submitButton.onclick = function() {
            window.open(imageUrl);  // Open image in new tab
        };

        // Save the image to the server when the save button is clicked
        saveButton.onclick = function() {
            const formData = new FormData();
            formData.append('image', file);  // Append the uploaded image to FormData

            fetch('/save_image', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    alert('Image saved successfully!');  // Success alert
                } else {
                    alert('Error saving image.');  // Error alert
                }
            })
            .catch(error => {
                console.error('Error:', error);  // Handle any errors during the fetch request
            });
        };
    }
});
