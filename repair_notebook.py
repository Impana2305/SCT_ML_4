import json
import os

with open("hand_gesture_recognition.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    source = "".join(cell["source"])
    
    # Fix the data loading cell
    if "class_to_idx = {class_name: idx for idx, class_name in enumerate(classes)}" in source:
        cell["source"] = [
            "IMG_SIZE = 64 # Resize all images to 64x64\n",
            "data = []\n",
            "labels = []\n",
            "classes_dict = {}\n",
            "class_index = 0\n",
            "\n",
            "if os.path.exists(DATASET_PATH):\n",
            "    for subject_folder in os.listdir(DATASET_PATH):\n",
            "        subject_path = os.path.join(DATASET_PATH, subject_folder)\n",
            "        if not os.path.isdir(subject_path): continue\n",
            "        \n",
            "        for gesture_folder in os.listdir(subject_path):\n",
            "            gesture_path = os.path.join(subject_path, gesture_folder)\n",
            "            if not os.path.isdir(gesture_path): continue\n",
            "                \n",
            "            if gesture_folder not in classes_dict:\n",
            "                classes_dict[gesture_folder] = class_index\n",
            "                class_index += 1\n",
            "                \n",
            "            current_class_idx = classes_dict[gesture_folder]\n",
            "            \n",
            "            for img_name in os.listdir(gesture_path):\n",
            "                img_path = os.path.join(gesture_path, img_name)\n",
            "                img = cv2.imread(img_path)\n",
            "                if img is None: continue\n",
            "                    \n",
            "                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))\n",
            "                data.append(img)\n",
            "                labels.append(current_class_idx)\n",
            "\n",
            "    classes = list(classes_dict.keys())\n",
            "    # Convert to numpy arrays\n",
            "    data = np.array(data, dtype='float32') / 255.0\n",
            "    labels = np.array(labels)\n",
            "\n",
            "    if len(labels) > 0:\n",
            "        labels = to_categorical(labels, num_classes=len(classes_dict))\n",
            "        print(f\"Data shape: {data.shape}\")\n",
            "        print(f\"Labels shape: {labels.shape}\")\n"
        ]
    
    # Fix the visualization cell
    elif "Visualize some training images" in source:
        cell["source"] = [
            "import matplotlib.pyplot as plt\n",
            "import random\n",
            "\n",
            "# Visualize some training images\n",
            "plt.figure(figsize=(12, 8))\n",
            "if os.path.exists(DATASET_PATH):\n",
            "    # Collect some valid image paths\n",
            "    sample_images = []\n",
            "    for subject_folder in os.listdir(DATASET_PATH):\n",
            "        subject_path = os.path.join(DATASET_PATH, subject_folder)\n",
            "        if not os.path.isdir(subject_path): continue\n",
            "        for gesture_folder in os.listdir(subject_path):\n",
            "            gesture_path = os.path.join(subject_path, gesture_folder)\n",
            "            if not os.path.isdir(gesture_path): continue\n",
            "            images = os.listdir(gesture_path)\n",
            "            if images:\n",
            "                sample_images.append((gesture_folder, os.path.join(gesture_path, random.choice(images))))\n",
            "    \n",
            "    if sample_images:\n",
            "        samples = random.sample(sample_images, min(5, len(sample_images)))\n",
            "        for i, (gesture_class, img_path) in enumerate(samples):\n",
            "            img = cv2.imread(img_path)\n",
            "            if img is not None:\n",
            "                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)\n",
            "                plt.subplot(1, len(samples), i + 1)\n",
            "                plt.imshow(img)\n",
            "                plt.title(gesture_class)\n",
            "                plt.axis('off')\n",
            "        plt.show()\n"
        ]

    # Fix the very first class exploration cell
    elif "Total classes found" in source and "class_path =" in source:
        cell["source"] = [
            "if os.path.exists(DATASET_PATH):\n",
            "    # Count total images per gesture across all subjects\n",
            "    gesture_counts = {}\n",
            "    for subject_folder in os.listdir(DATASET_PATH):\n",
            "        subject_path = os.path.join(DATASET_PATH, subject_folder)\n",
            "        if not os.path.isdir(subject_path): continue\n",
            "        for gesture_folder in os.listdir(subject_path):\n",
            "            gesture_path = os.path.join(subject_path, gesture_folder)\n",
            "            if not os.path.isdir(gesture_path): continue\n",
            "            gesture_counts[gesture_folder] = gesture_counts.get(gesture_folder, 0) + len(os.listdir(gesture_path))\n",
            "            \n",
            "    print(f\"Total unique gestures found: {len(gesture_counts)}\")\n",
            "    for gesture, count in gesture_counts.items():\n",
            "        print(f\" - {gesture}: {count} images total\")\n",
            "else:\n",
            "    print(\"Dataset path not found. Please update DATASET_PATH.\")\n"
        ]

with open("hand_gesture_recognition.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)
