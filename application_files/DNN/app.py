from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load the image classification model
image_model_path = 'D:/Downloads/Flask/flask/DNN_image.h5'  # Update with the correct path to your image classification model
image_model = load_model(image_model_path)

# Dictionary of class labels
class_labels = {0: 'drink', 1: 'food', 2: 'inside', 3: 'menu', 4: 'outside'}

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to preprocess images
def preprocess_image(image_path):
    logging.info(f"Preprocessing image: {image_path}")
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize to the input size expected by the model
    img_array = np.array(img) / 255.0  # Normalize to [0, 1] range
    img_array = img_array.reshape((1, 224, 224, 3))  # Reshape for the model (batch size of 1)
    return img_array

@app.route('/')
def index():
    """Render the HTML page."""
    return render_template('index.html')

# Route to handle image label prediction
@app.route('/predict_image_label', methods=['POST'])
def predict_image_label():
    """Handle the image label prediction."""
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Preprocess the image for model prediction
        img_array = preprocess_image(file_path)

        # Make prediction using the image model
        prediction = image_model.predict(img_array)
        predicted_class_index = np.argmax(prediction, axis=1)[0]  # Get the predicted index

        # Get the corresponding label from the class_labels dictionary
        predicted_label = class_labels.get(predicted_class_index, "Unknown")

        # Return the predicted label
        return jsonify({"label": str(predicted_label)}), 200

if __name__ == '__main__':
    app.run(debug=True)
