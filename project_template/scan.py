import os

from project_template.util import scan_args_for_string, whether_ignore_file


__all__ = ["scan_directory", "scan_args"]


def scan_directory(directory: str, ignore_files: list):
    """
    @brief      扫描目录
    @details    扫描目录中的所有文件和目录，并返回，格式如下
    ```python
    [
        {
            "name":     "file_name",    # 文件名, basename
            "type":     "file",         # 文件类型, file或者directory
            "root":     "file_path",    # 文件所在目录，相对于项目根目录
            "mode":     "file_mode",    # 文件的权限模式
            "content":  "file_content", # 文件的内容
        },
        {
            "name":     "dir_name",     # 目录名, basename   
            "type":     "dir",          # 目录类型, directory
            "root":     "dir_path",     # 目录所在目录，相对于项目根目录
            "mode":     "dir_mode",     # 目录的权限模式
            "content":  None,           # 目录内容默认是 None
        },
    ]
    ```

    @param directory 目录路径
    @param ignore_files 忽略的文件列表
    @return 目录中的所有文件和目录
    """
    if not os.path.exists(directory):
        raise ValueError(f"Directory does not exist: {directory}")
    if not os.path.isdir(directory):
        raise ValueError(f"Not a directory: {directory}")

    directory = os.path.abspath(directory)
    dirs_and_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            name = file
            type_ = "file"
            relative_root = os.path.relpath(root, directory)
            path = os.path.join(root, file)

            to_continue = False
            for ignore_file in ignore_files:
                if whether_ignore_file(path, ignore_file):
                    to_continue = True
                    break
            if to_continue:
                continue

            file_mode = os.stat(path).st_mode
            with open(path, "r") as f:
                content = f.read()
            dirs_and_files.append({
                "name": name,
                "type": type_,
                "root": relative_root,
                "mode": file_mode,
                "content": content,
            })
        for dir in dirs:
            name = dir
            type_ = "dir"
            relative_root = os.path.relpath(root, directory)
            path = os.path.join(root, dir)

            to_continue = False
            for ignore_file in ignore_files:
                if whether_ignore_file(path, ignore_file):
                    to_continue = True
                    break
            if to_continue:
                continue

            dir_mode = os.stat(path).st_mode
            dirs_and_files.append({
                "name": name,
                "type": type_,
                "root": relative_root,
                "mode": dir_mode,
                "content": None,
            })

    return dirs_and_files


def print_dirs_and_files(dirs_and_files: list):
    """
    @brief  打印目录和文件

    @param dirs_and_files 目录和文件列表
    """
    file_tree = {}
    for dir_or_file in dirs_and_files:
        path = os.path.join(dir_or_file["root"], dir_or_file["name"])
        if path.startswith("./"):
            path = path[2:]

        parts = path.split(os.sep)
        current = file_tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        if dir_or_file["type"] == "dir":
            current[parts[-1]] = {}
        else:
            current[parts[-1]] = dir_or_file["content"]

    def print_tree(node, prefix=''):
        keys = sorted(node.keys())
        for i, key in enumerate(keys):
            if isinstance(node[key], dict):
                sub_node = node[key]

                colored_key = f"\033[34m{key}\033[0m"
                print(f"{prefix}├── {colored_key}/")
                extension = '    '
                print_tree(sub_node, prefix + extension)
            else:
                colored_key = f"\033[32m{key}\033[0m"
                print(f"{prefix}├── {colored_key}")

    print_tree(file_tree)


def check_args(args: list):
    """
    @brief  检查参数是否存在冲突，如参数名称相同，但默认值不同

    @param  args 参数列表
    @throw  RuntimeError 参数名称冲突
    """
    args_dict = {}
    for arg in args:
        arg_name = arg["name"]
        default_value = arg["default_value"]
        root = arg["root"]
        path = os.path.join(root, arg_name)
        type_ = arg["type"]
        if default_value is None:
            continue
        elif arg_name not in args_dict:
            args_dict[arg_name] = {
                "default_value": default_value,
                "path": path,
                "type": type_,
            }
        else:
            if args_dict[arg_name]["default_value"] == default_value:
                continue
            
            first_path = args_dict[arg_name]["path"]
            first_type = args_dict[arg_name]["type"]

            message = f"Default value conflict for argument: {arg_name}. check {first_type} in {first_path} and {type_} in {path}"
            raise RuntimeError(f"Default value conflict for argument: {arg_name}")
        

def filter_args(args: list):
    """
    @brief  过滤重复参数，获取参数以及默认值

    @param  args 参数列表
    @return 过滤后的参数列表
    """
    args_dict = {}
    for arg in args:
        arg_name = arg["name"]
        default_value = arg["default_value"]
        if arg_name not in args_dict:
            args_dict[arg_name] = default_value
        elif args_dict[arg_name] is None:
            args_dict[arg_name] = default_value

    args = [
        {
            "name": arg_name,
            "default_value": default_value,
        }
        for arg_name, default_value in args_dict.items()
    ]
    return args


def scan_args(directories_and_files: list):
    """
    @brief      扫描目录中的参数
    @details    扫描目录中的参数，并返回参数列表，参数列表中包含参数名称、默认值、参数所在位置

    @param  directories_and_files 目录中的所有文件和目录
    @return 所有参数
    """
    args = []
    for directory_or_file in directories_and_files:
        dir_or_file_args = []
        name = directory_or_file.get("name", None)
        root = directory_or_file.get("root", None)
        content = directory_or_file.get("content", None)

        name_args = scan_args_for_string(name)
        content_args = []
        if content is not None:
            content_lines = content.split("\n")
            for line in content_lines:
                line_args = scan_args_for_string(line)
                content_args.extend(line_args)

        dir_or_file_args = []
        for arg in name_args + content_args:
            arg_name = arg["name"]
            dir_or_file_args.append(arg_name)
        directory_or_file["arguments"] = dir_or_file_args

        for arg in name_args:
            arg_name = arg["name"]
            arg_default_value = arg["default_value"]
            arg_type = "file_name"

            arg = {
                "name": arg_name,
                "default_value": arg_default_value,
                "type": arg_type,
                "root": root,
            }
            args.append(arg)
        for arg in content_args:
            arg_name = arg["name"]
            arg_default_value = arg["default_value"]
            arg_type = "file_content"

            arg = {
                "name": arg_name,
                "default_value": arg_default_value,
                "type": arg_type,
                "root": root,
            }
            args.append(arg)

    check_args(args)
    args = filter_args(args)
    return args


def main():
    example_dir = "./examples/dl_model"
    files_and_dirs = scan_directory(example_dir)
    args = scan_args(files_and_dirs)
    print(args)


if __name__ == "__main__":
    main()
