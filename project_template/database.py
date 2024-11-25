import os
import re
from project_template.scan import scan_directory, scan_args
from project_template.constants import DATABASE_FILE, DEFAULT_TEMPLATE_DIR, TEMPLATE_NAME_REGEX
from project_template.util import save_write_json, save_read_json


__all__ = ["add_template", "delete_template", "update_template", "get_template", "list_template_names"]



def add_template(name, project_dir, location_dir=DEFAULT_TEMPLATE_DIR, ignore_files=[]):
    """
    @brief  根据项目模板创建项目

    @param name         项目模板名称
    @param project_dir  项目模板路径
    @param location_dir 项目模板存放位置
    @param ignore_files 忽略文件列表
    """
    project_dir = os.path.abspath(project_dir)
    location_dir = os.path.abspath(location_dir)
    template_pattern = re.compile(TEMPLATE_NAME_REGEX)
    if not template_pattern.match(name):
        raise ValueError(f"Invalid template name: {name}")
    
    if not os.path.exists(project_dir):
        raise ValueError(f"Project directory does not exist: {project_dir}")
    if not os.path.isdir(project_dir):
        raise ValueError(f"Project directory is not a directory: {project_dir}")
    
    if not os.path.exists(location_dir):
        os.makedirs(location_dir)
    if not os.path.isdir(location_dir):
        raise ValueError(f"Location directory is not a directory: {location_dir}")
    
    if not os.path.exists(DATABASE_FILE):
        save_write_json(DATABASE_FILE, {})

    database = save_read_json(DATABASE_FILE)

    if name in database:
        raise ValueError(f"Template already exists: {name}. If you want to update the template, please use update_template function.")

    dirs_and_files = scan_directory(project_dir, ignore_files)
    args = scan_args(dirs_and_files)
    config = {
        "dirs_and_files": dirs_and_files,
        "args": args,
    }
    config_file = os.path.join(location_dir, f"{name}.json")
    save_write_json(config_file, config)

    database[name] = {
        "project_dir": project_dir,
        "location": location_dir,
        "config_file": config_file,
    }
    save_write_json(DATABASE_FILE, database)


def delete_template(name):
    """
    @brief  删除项目模板

    @param name 项目模板名称
    """
    if not os.path.exists(DATABASE_FILE):
        save_write_json(DATABASE_FILE, {})
    database = save_read_json(DATABASE_FILE)
    if name not in database:
        raise ValueError(f"Template does not exist: {name}")
    
    config_file = database[name]["config_file"]
    config = save_read_json(config_file)
    os.remove(config_file)

    data = database.pop(name)
    project_dir = data["project_dir"]
    save_write_json(DATABASE_FILE, database)

    return project_dir, config


def update_template(name, project_dir, location_dir=DEFAULT_TEMPLATE_DIR, ignore_files=[]):
    """
    @brief  更新项目模板

    @param name         项目模板名称
    @param project_dir  项目模板路径
    """
    delete_template(name)
    add_template(name, project_dir, location_dir, ignore_files)


def get_template(name):
    """
    @brief  获取项目模板

    @param name 项目模板名称
    """
    if not os.path.exists(DATABASE_FILE):
        save_write_json(DATABASE_FILE, {})
    database = save_read_json(DATABASE_FILE)
    if name not in database:
        raise ValueError(f"Template does not exist: {name}")
    
    config_file = database[name]["config_file"]
    project_dir = database[name]["project_dir"]
    config = save_read_json(config_file)
    
    return project_dir, config


def list_template_names():
    """
    @brief  列出所有项目模板名称
    """
    if not os.path.exists(DATABASE_FILE):
        save_write_json(DATABASE_FILE, {})
    database = save_read_json(DATABASE_FILE)
    names = list(database.keys())
    return names


def generate_template(project_dir, template_dir, rules: dict):
    """
    @brief  根据配置文件和现有项目生成项目模板

    @param project_dir  现有项目路径
    @param template_dir 项目模板存放位置
    @param rules        规则说明
    """
    project_dir = os.path.abspath(project_dir)
    template_dir = os.path.abspath(template_dir)
    if not os.path.exists(project_dir):
        raise ValueError(f"Project directory does not exist: {project_dir}")
    if not os.path.isdir(project_dir):
        raise ValueError(f"Project directory is not a directory: {project_dir}")
    
    if os.path.exists(template_dir):
        raise ValueError(f"Template directory already exists: {template_dir}")
    else:
        os.makedirs(template_dir)

    ignore_files = rules.get("ignore_files", [])
    rules = rules.get("rules", [])
    
    dirs_and_files = scan_directory(project_dir, ignore_files)

    for dir_or_file in dirs_and_files:
        name = dir_or_file["name"]
        type_ = dir_or_file["type"]
        root = dir_or_file["root"]
        mode = dir_or_file["mode"]
        content = dir_or_file["content"]

        file_path = os.path.join(root, name)

        if type_ == "file":
            for rule in rules:
                value_name = rule.get("value_name", None)
                if value_name is None:
                    continue

                default_value = rule.get("default_value", None)
                if default_value is None:
                    replace_name = f"#{{{value_name}}}"
                else:
                    replace_name = f"#{{{value_name}:{default_value}}}"
                file_path = file_path.replace(value_name, replace_name)
                content = content.replace(value_name, replace_name)
            
            new_file_path = os.path.join(template_dir, file_path)
            with open(new_file_path, "w") as f:
                f.write(content)

        elif type_ == "dir":
            for rule in rules:
                value_name = rule.get("value_name", None)
                if value_name is None:
                    continue
                
                default_value = rule.get("default_value", None)
                if default_value is None:
                    replace_name = f"#{{{value_name}}}"
                else:
                    replace_name = f"#{{{value_name}:{default_value}}}"
                file_path = file_path.replace(value_name, replace_name)
            
            new_dir_path = os.path.join(template_dir, file_path)
            os.makedirs(new_dir_path, exist_ok=True)


def main():
    add_template("test", "./examples/dl_model")


if __name__ == "__main__":
    main()
