import json
import os

with open("hand_gesture_recognition.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# Find the explore dataset section to insert plotting code
explore_idx = -1
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "markdown" and "Explore the Dataset" in "".join(cell["source"]):
        explore_idx = i
        break

if explore_idx != -1:
    plot_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import matplotlib.pyplot as plt\n",
            "import random\n",
            "\n",
            "# Visualize some training images\n",
            "plt.figure(figsize=(12, 8))\n",
            "if os.path.exists(DATASET_PATH):\n",
            "    sample_classes = random.sample(classes, min(5, len(classes)))\n",
            "    for i, gesture_class in enumerate(sample_classes):\n",
            "        class_path = os.path.join(DATASET_PATH, gesture_class)\n",
            "        if os.path.isdir(class_path):\n",
            "            images = os.listdir(class_path)\n",
            "            if images:\n",
            "                img_name = random.choice(images)\n",
            "                img_path = os.path.join(class_path, img_name)\n",
            "                img = cv2.imread(img_path)\n",
            "                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)\n",
            "                plt.subplot(1, len(sample_classes), i + 1)\n",
            "                plt.imshow(img)\n",
            "                plt.title(gesture_class)\n",
            "                plt.axis('off')\n",
            "    plt.show()"
        ]
    }
    nb["cells"].insert(explore_idx + 2, plot_cell)

# Find the test image cell
test_idx = -1
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code" and "NEW_IMAGE_PATH =" in "".join(cell["source"]):
        test_idx = i
        break

if test_idx != -1:
    test_plot_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "if os.path.exists(NEW_IMAGE_PATH) and len(data) > 0:\n",
            "    img = cv2.imread(NEW_IMAGE_PATH)\n",
            "    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)\n",
            "    \n",
            "    plt.figure(figsize=(6, 6))\n",
            "    plt.imshow(img)\n",
            "    plt.title(f\"Predicted: {label} ({conf*100:.2f}%)\")\n",
            "    plt.axis('off')\n",
            "    plt.show()"
        ]
    }
    nb["cells"].insert(test_idx + 1, test_plot_cell)

with open("hand_gesture_recognition.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)