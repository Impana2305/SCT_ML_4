import json

with open("hand_gesture_recognition.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    source = "".join(cell["source"])
    
    # Fix the data loading cell to define idx_to_class
    if "data = np.array(data, dtype='float32') / 255.0" in source:
        new_source = source.replace(
            "classes = list(classes_dict.keys())",
            "classes = list(classes_dict.keys())\n    idx_to_class = {v: k for k, v in classes_dict.items()}\n"
        )
        cell["source"] = [line + "\n" if not line.endswith("\n") else line for line in new_source.split("\n") if line]

with open("hand_gesture_recognition.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)
