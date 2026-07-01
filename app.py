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
            
        # Try to detect and crop hand using skin color thresholding
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Find contours of the skin mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour (assuming it's the hand)
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 500: # Threshold for minimum hand size
                # Apply mask to the original image to black out background
                img = cv2.bitwise_and(img, img, mask=mask)
                
                x, y, w_c, h_c = cv2.boundingRect(c)
                
                # Add padding
                pad_x = int(w_c * 0.2)
                pad_y = int(h_c * 0.2)
                
                h, w, _ = img.shape
                x_min = max(0, x - pad_x)
                y_min = max(0, y - pad_y)
                x_max = min(w, x + w_c + pad_x)
                y_max = min(h, y + h_c + pad_y)
                
                # Make square crop
                cx = (x_min + x_max) // 2
                cy = (y_min + y_max) // 2
                side = max(x_max - x_min, y_max - y_min) // 2
                
                crop_x_min = max(0, cx - side)
                crop_y_min = max(0, cy - side)
                crop_x_max = min(w, cx + side)
                crop_y_max = min(h, cy + side)
                
                if crop_y_max > crop_y_min and crop_x_max > crop_x_min:
                    img = img[crop_y_min:crop_y_max, crop_x_min:crop_x_max]

        # Convert to grayscale to simulate near-IR images in dataset, then back to 3-channel
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        # Preprocess
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
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
