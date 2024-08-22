import os
import json
import copy
import warnings
from project_template.constants import DATABASE_FILE


def get_template(name):
    with open(DATABASE_FILE, "r") as f:
        configs = json.load(f)

    config = configs.get(name, None)
    if config is None:
        raise ValueError(f"Template {name} not found")
    
    location = config.get("location", None)
    config_path = config.get("config_path", None)

    if location is None:
        warnings.warn("location is null, please delete the template")
        raise ValueError("location is None")
    if config_path is None:
        warnings.warn("config_path is null, please delete the template")
        raise ValueError("config_path is None")
    
    with open(config_path, "r") as f:
        configs = json.load(f)

    return location, configs


def update_configs(location, project_dir, configs, config_args):
    new_configs = copy.deepcopy(configs)

    num_configs = len(configs)
    for i in range(len(configs)):
        config = configs[i]
        new_config = new_configs[i]
        config_file_system_arg, config_file_content_arg = config_args[i]

        instance_name = name = config.get("name")
        type_ = config.get("type")
        root = config.get("root")
        file_system_args = config.get("file_system_args")
        file_content_args = config.get("file_content_args")

        if type_ == "dir":
            for arg in file_system_args:
                file_system_default_value = arg.get("default_value", None)
                file_system_instance = arg.get("instance", None)
                file_system_name = arg.get("name", None)
                file_system_value = config_file_system_arg.get(file_system_name, file_system_default_value)
                instance_name = instance_name.replace(file_system_instance, file_system_value)

            new_config["name"] = instance_name
            child_root = os.path.join(root, name)
            instance_child_root = os.path.join(root, instance_name)

            for j in range(i + 1, num_configs):
                child_config = new_configs[j]
                root = child_config.get("root")
                if root[:len(child_root)] == child_root:
                    new_configs[j]["root"] = instance_child_root + root[len(child_root):]

        elif type_ == "file":
            for arg in file_system_args:
                file_system_default_value = arg.get("default_value", None)
                file_system_instance = arg.get("instance", None)
                file_system_name = arg.get("name", None)
                file_system_value = config_file_system_arg.get(file_system_name, file_system_default_value)
                instance_name = instance_name.replace(file_system_instance, file_system_value)

            new_config["name"] = instance_name
            file_path = os.path.join(root, name)
            with open(file_path) as f:
                content = f.read()

            for arg in file_content_args:
                file_content_default_value = arg.get("default_value", None)
                file_content_instance = arg.get("instance", None)
                file_content_name = arg.get("name", None)
                file_content_value = config_file_content_arg.get(file_content_name, file_content_default_value)
                content = content.replace(file_content_instance, file_content_value)

            new_config["content"] = content

        else:
            raise ValueError(f"Invalid type: {type_}")
        
    for new_config in new_configs:
        root = new_config.get("root")
        root = project_dir + root[len(location):]
        new_config["root"] = root
    
    return new_configs


def generate_project(template_name, project_dir, config_args):
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    else:
        raise ValueError(f"Project directory {project_dir} already exists")
    
    location, configs = get_template(template_name)
    new_configs = update_configs(location, project_dir, configs, config_args)
    for new_config in new_configs:
        name = new_config.get("name")
        type_ = new_config.get("type")
        root = new_config.get("root")
        mode = new_config.get("mode")
        content = new_config.get("content")

        path = os.path.join(root, name)
        if type_ == "dir":
            os.makedirs(path, exist_ok=True)
        elif type_ == "file":
            with open(path, "w") as f:
                f.write(content)
        else:
            raise ValueError(f"Invalid type: {type_}")
        
        os.chmod(path, mode)


def main():
    location, configs = get_template("test")
    config_args = []
    for i in range(len(configs)):
        config = configs[i]
        name = config.get("name")
        type_ = config.get("type")
        root = config.get("root")
        mode = config.get("mode")
        file_system_args = config.get("file_system_args")
        file_content_args = config.get("file_content_args")

        config_file_system_arg = {}
        config_file_content_arg = {}
        for arg in file_system_args:
            default_value = arg.get("default_value", None)
            instance = arg.get("instance", None)
            name_ = arg.get("name", None)

            input_message = f"file system variable {name_}(default: {default_value}) in {root}/{name} need to be set: "
            value = input(input_message)
            if value.strip() == "":
                value = default_value
            config_file_system_arg[name_] = value
        for arg in file_content_args:
            default_value = arg.get("default_value", None)
            instance = arg.get("instance", None)
            name_ = arg.get("name", None)

            input_message = f"file content variable {name_}(default: {default_value}) in {root}/{name} need to be set: "
            value = input(input_message)
            if value.strip() == "":
                value = default_value
            config_file_content_arg[name_] = value

        config_args.append((config_file_system_arg, config_file_content_arg))

    project_dir = "/mnt/hd1/moyuzai/projects/test"
    generate_project("test", project_dir, config_args)
    # new_configs = update_configs(location, project_dir, configs, config_args)
    # for i, new_config in enumerate(new_configs):
    #     print(i, new_config)

if __name__ == "__main__":
    main()