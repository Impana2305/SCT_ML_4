import json
import re

with open("hand_gesture_recognition.ipynb", "r", encoding="utf-8") as f:
    notebook = json.load(f)

new_cells = []
for cell in notebook.get("cells", []):
    if cell["cell_type"] == "markdown":
        text = "".join(cell.get("source", []))
        if "Provide the path to your dataset below" in text:
            continue
    elif cell["cell_type"] == "code":
        source = cell.get("source", [])
        new_source = []
        for line in source:
            if "# UPDATE THIS PATH to where your dataset is extracted" in line:
                continue
            if "Dataset path not found. Please update DATASET_PATH." in line:
                line = line.replace("Dataset path not found. Please update DATASET_PATH.", "Dataset path not found.")
            if "NEW_IMAGE_PATH =" in line and "Update this path" in line:
                line = "NEW_IMAGE_PATH = 'path_to_test_image.jpg'\n"
            if "Please provide a valid path to an image in NEW_IMAGE_PATH to test." in line:
                line = line.replace(" in NEW_IMAGE_PATH", "")
            new_source.append(line)
        cell["source"] = new_source
    new_cells.append(cell)

notebook["cells"] = new_cells

with open("hand_gesture_recognition.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)
