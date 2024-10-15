from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the pre-trained models
xgb_model_parking = joblib.load('model/xgboost_model.pkl')
dnn_model1=joblib.load('model/DNN_txt.pkl')

def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((64, 64))
    img = np.array(img) / 255.0
    img = img.reshape(1, 64, 64, 3)
    return img

def preprocess_business_data(data):
    features = np.array([float(x) for x in data.split(',')])
    return features.reshape(1, -1)

@app.route('/predict_parking', methods=['POST'])
def predict_parking():
    business_data = request.form['business_data']
    features = preprocess_business_data(business_data)

    # Predict using the XGBoost model
    xgb_prediction = xgb_model_parking.predict(features)
    dnn_model = dnn_model1.predict(features)

    # Combine results as if they are from two models
    result = {
        "xgb_parking": int(xgb_prediction[0]),
        "dnn_prediction": int(dnn_model[0])  
    }

    return jsonify({"prediction": result})




@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  
