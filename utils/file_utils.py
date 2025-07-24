
import os
import json

DATA_DIR = "saved_projects"

def save_project_data(project_name, references, decisions):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{project_name}.json")
    with open(path, "w") as f:
        json.dump({"references": references, "decisions": decisions}, f)

def load_project_data(project_name):
    path = os.path.join(DATA_DIR, f"{project_name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["references"], data["decisions"]
    return [], {}
