import os
import json
import shutil
from project_template.scan import scan_dir
from project_template.constants import DATABASE_FILE, DEFAULT_TEMPLATE_DIR


def copy_dir(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_dir(s, d)
        else:
            shutil.copy2(s, d)


def create_template(name, project_dir, location_dir=DEFAULT_TEMPLATE_DIR):
    project_dir = os.path.abspath(os.path.realpath(project_dir))
    if not os.path.isdir(project_dir):
        raise ValueError(f"{project_dir} is not a directory")
    
    location_dir = location_dir.rstrip("/")
    if not os.path.exists(location_dir):
        os.makedirs(location_dir)
    if not os.path.isdir(location_dir):
        raise ValueError(f"{location_dir} is not a directory")

    location = os.path.join(location_dir, name)
    if not os.path.exists(location):
        os.makedirs(location)
    else:
        raise ValueError(f"{location} already exists")

    copy_dir(project_dir, location)

    configs = scan_dir(project_dir)
    project_dir_len = len(project_dir)
    for config in configs:
        root = config.get("root", None)
        if root is None:
            raise ValueError("root is None")
        root = location+root[project_dir_len:]
        config["root"] = root

    config_path = os.path.join(location_dir, f"{name}.json")
    with open(config_path, "w") as f:
        json.dump(configs, f, indent=4)
    
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as f:
            json.dump({
                name: {
                    "location": location,
                    "config_path": config_path,
                }
            }, f, indent=4)
    else:
        with open(DATABASE_FILE, "r") as f:
            database = json.load(f)
        database[name] = {
            "location": location,
            "config_path": config_path,
        }
        with open(DATABASE_FILE, "w") as f:
            json.dump(database, f, indent=4)


def main():
    create_template("test", "./examples/dl_model")


if __name__ == "__main__":
    main()
