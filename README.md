# Hand Gesture Recognition CNN 🖐️

**Task 04** of the SkillCraft Technology Machine Learning Internship.

This project implements a Convolutional Neural Network (CNN) to recognize and classify hand gestures from images. It features a complete pipeline from data preprocessing to model training, and includes a modern, beautifully designed React frontend to easily test the model.

## 📁 Dataset
This project uses the **leapGestRecog** dataset, which contains near-infrared images of hand gestures.
- The dataset is structured into 10 distinct classes: `01_palm`, `02_l`, `03_fist`, `04_fist_moved`, `05_thumb` (thumbs up), `06_index`, `07_ok`, `08_palm_moved`, `09_c`, `10_down`.
- Images are preprocessed by resizing to 64x64, converting to grayscale (then to 3-channel to match model requirements), and normalizing pixel values.

## 🧠 Model Architecture
The model is a robust CNN built with TensorFlow/Keras, consisting of:
- **3 Convolutional Layers** (with ReLU activation and MaxPooling) to extract spatial features from the hand gestures.
- **Flatten Layer** to convert 2D feature maps to 1D.
- **Dense Layers** with Dropout (0.5) to prevent overfitting.
- **Softmax Output Layer** to classify into the 10 gesture categories.

## 🛠️ Tech Stack
- **Machine Learning**: Python, TensorFlow, Keras, OpenCV, Scikit-learn
- **Backend API**: Flask
- **Frontend**: React, Vite, standard CSS (fully responsive, modern UI)

## 🚀 How to Run Locally

### 1. Start the Backend API
The Python backend processes the image using skin-color thresholding and runs inference through the trained CNN model.
```bash
# Install dependencies
pip install tensorflow opencv-python flask flask-cors numpy scikit-learn

# Run the backend (runs on http://localhost:5000)
python app.py
```

### 2. Start the Frontend UI
The modern React application provides an intuitive drag-and-drop interface for testing the model.
```bash
cd frontend

# Install frontend dependencies
npm install

# Start the Vite development server
npm run dev
```
Open the provided localhost URL in your browser to test the gesture recognition.

## 📊 Results
The model achieves high accuracy on the test set. When testing with real-world images (like from a webcam or Google), the backend automatically uses skin-color thresholding to isolate the hand and black out the background, ensuring high prediction accuracy that perfectly matches the training distribution.
