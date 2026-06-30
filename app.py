import os
import cv2
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'model.keras'
CLASSES_PATH = 'classes.json'

model = None
classes_dict = {}

IMG_SIZE = 64

def load_model_and_classes():
    global model, classes_dict
    if os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH):
        model = load_model(MODEL_PATH)
        with open(CLASSES_PATH, 'r') as f:
            classes_dict = json.load(f)
        print("Model and classes loaded successfully.")
    else:
        print("Error: model.keras or classes.json not found. Please train the model first.")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model is not loaded."}), 500
        
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request."}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400
        
    try:
        # Read the image via cv2
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image."}), 400
            
        # Preprocess
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0) # Add batch dimension
        
        # Predict
        prediction = model.predict(img)
        predicted_class_idx = np.argmax(prediction[0])
        confidence = float(prediction[0][predicted_class_idx])
        
        predicted_class_name = classes_dict.get(str(predicted_class_idx), "Unknown")
        
        # Make name prettier (e.g. "01_palm" -> "Palm")
        pretty_name = predicted_class_name.split('_', 1)[-1].replace('_', ' ').title()
        
        return jsonify({
            "gesture": pretty_name,
            "raw_class": predicted_class_name,
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_model_and_classes()
    app.run(debug=True, port=5000)
