import os
import cv2
import numpy as np
import json

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

DATASET_PATH = r'D:\leapGestRecog'
IMG_SIZE = 64

data = []
labels = []
classes_dict = {}
class_index = 0

print("Loading dataset...")
if os.path.exists(DATASET_PATH):
    # Iterate through subject folders (00, 01, 02, etc.)
    for subject_folder in os.listdir(DATASET_PATH):
        subject_path = os.path.join(DATASET_PATH, subject_folder)
        if not os.path.isdir(subject_path): continue
            
        # Iterate through gesture folders
        for gesture_folder in os.listdir(subject_path):
            gesture_path = os.path.join(subject_path, gesture_folder)
            if not os.path.isdir(gesture_path): continue
                
            # Manage classes
            if gesture_folder not in classes_dict:
                classes_dict[gesture_folder] = class_index
                class_index += 1
                
            current_class_idx = classes_dict[gesture_folder]
            
            # Iterate through images
            for img_name in os.listdir(gesture_path):
                img_path = os.path.join(gesture_path, img_name)
                
                img = cv2.imread(img_path)
                if img is None: continue
                    
                # Resize and convert to RGB (cv2 loads as BGR)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                data.append(img)
                labels.append(current_class_idx)
                
print(f"Loaded {len(data)} images across {len(classes_dict)} classes.")

# Prepare arrays
data = np.array(data, dtype='float32') / 255.0
labels = np.array(labels)
num_classes = len(classes_dict)

labels = to_categorical(labels, num_classes=num_classes)

print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

print("Building model...")
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("Training model...")
EPOCHS = 10
BATCH_SIZE = 32

model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test, y_test))

print("Saving model and class mappings...")
model.save('model.keras')

idx_to_class = {v: k for k, v in classes_dict.items()}
with open('classes.json', 'w') as f:
    json.dump(idx_to_class, f)

print("Training complete! Model saved to model.keras and classes saved to classes.json")
