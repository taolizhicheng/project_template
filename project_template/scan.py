import os
import re


__all__ = ["scan_dir"]


ARG_REGEX = re.compile(r"\#\{\w+:\S+\}|\#\{\w+\}")


def walk_dir(dir_path):
    dir_path = os.path.abspath(dir_path)
    dirs_and_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            path = os.path.join(root, file)
            file_mode = os.stat(path).st_mode
            file = {
                "name": file,
                "type": "file",
                "root": root,
                "mode": file_mode,
            }
            dirs_and_files.append(file)
        for dir in dirs:
            path = os.path.join(root, dir)
            dir_mode = os.stat(path).st_mode
            dir = {
                "name": dir,
                "type": "dir",
                "root": root,
                "mode": dir_mode,
            }
            dirs_and_files.append(dir)
    return dirs_and_files


def scan_string_pattern(string):
    found_args = ARG_REGEX.findall(string)
    filtered_names = []
    filtered_args = []
    for arg_instance in found_args:
        arg_name = arg_instance[2:-1]
        if ":" in arg_instance:
            arg_name, default_value = arg_name.split(":")
        else:
            default_value = None

        if arg_name in filtered_names:
            index = filtered_names.index(arg_name)
            if filtered_args[index]["default_value"] is None:
                filtered_args[index]["default_value"] = default_value
        else:
            filtered_names.append(arg_name)
            filtered_args.append({
                "default_value": default_value,
                "instance": arg_instance,
                "name": arg_name,
            })
    return filtered_args


def scan_dir_or_file_args(dir_or_file):
    name = dir_or_file.get("name", None)
    type_ = dir_or_file.get("type", None)
    root = dir_or_file.get("root", None)
    path = os.path.join(root, name)
    mode = dir_or_file.get("mode", None)

    args = {
        "name": name,
        "type": type_,
        "root": root,
        "mode": mode,
        "file_system_args": [],
        "file_content_args": [],
    }

    if type_ == "file":
        args["file_system_args"] = scan_string_pattern(name)
        with open(path, "r") as f:
            content = f.read()
            args["file_content_args"] = scan_string_pattern(content)
    elif type_ == "dir":
        args["file_system_args"] = scan_string_pattern(name)
    else:
        raise ValueError(f"Invalid type: {type_}")
    return args


def scan_dir(dir_path):
    dirs_and_files = walk_dir(dir_path)
    all_args = []
    for dir_or_file in dirs_and_files:
        args = scan_dir_or_file_args(dir_or_file)
        all_args.append(args)
    return all_args


def main():
    example_dir = "./examples/dl_model"
    all_args = scan_dir(example_dir)
    for args in all_args:
        print(args)


if __name__ == "__main__":
    main()
