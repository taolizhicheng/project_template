import os
import json
import shutil
import warnings
from project_template.constants import DATABASE_FILE


def delete_template(name):
    if not os.path.exists(DATABASE_FILE):
        warnings.warn(f"{DATABASE_FILE} does not exist")
        return
    
    with open(DATABASE_FILE, "r") as f:
        templates = json.load(f)
    
    if name not in templates:
        raise ValueError(f"{name} does not exist")
    
    template = templates.pop(name)
    location = template.get("location")
    config_path = template.get("config_path")
    if os.path.exists(config_path):
        os.remove(config_path)
    if os.path.exists(location):
        shutil.rmtree(location)

    with open(DATABASE_FILE, "w") as f:
        json.dump(templates, f, indent=4)


def main():
    delete_template("test")


if __name__ == "__main__":
    main()
