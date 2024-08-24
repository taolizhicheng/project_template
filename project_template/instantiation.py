import os
from project_template.database import get_template
from project_template.util import is_directory_empty, format_string


def instantiate_project(name, project_dir, args):
    """
    @brief  实例化项目

    @param name         项目模板名称
    @param project_dir  项目目录
    @param args         配置参数
    """
    _, configs = get_template(name)
    
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    elif not os.path.isdir(project_dir):
        raise ValueError(f"Project directory {project_dir} is not a directory")
    elif not is_directory_empty(project_dir):
        raise ValueError(f"Project directory {project_dir} is not empty, which may rewrite the existing files.")
    
    expected_args = configs.get("args", None)
    final_args = {}
    for arg in expected_args:
        name = arg["name"]
        default = arg["default_value"]

        if name not in args and default is None:
            raise ValueError(f"Missing required argument: {name}")
        
        if name not in args:
            final_args[name] = default
        else:
            final_args[name] = args[name]
    
    dirs_and_files = configs.get("dirs_and_files", [])
    for dir_or_file in dirs_and_files:
        name = dir_or_file["name"]
        type_ = dir_or_file["type"]
        root = dir_or_file["root"]
        mode = dir_or_file["mode"]
        content = dir_or_file["content"]

        path = os.path.join(project_dir, root, name)
        path = format_string(path, args)
        if content is not None:
            content_lines = content.split("\n")
            for i in range(len(content_lines)):
                content_lines[i] = format_string(content_lines[i], args)
            content = "\n".join(content_lines)

        if type_ == "file":
            with open(path, "w") as f:
                f.write(content)
        elif type_ == "dir":
            os.makedirs(path)
        else:
            raise TypeError(f"Invalid type: {type_}")
        
        os.chmod(path, mode)


def main():
    instantiate_project("test", "/tmp/test", {})


if __name__ == "__main__":
    main()