import os
import sys
import tempfile
import subprocess
import argparse

from project_template.scan import print_dirs_and_files
from project_template.database import add_template, update_template, delete_template, get_template, list_template_names
from project_template.instantiation import instantiate_project
from project_template.constants import EDITOR, DEFAULT_TEMPLATE_DIR


def get_values(init_message):
    init_message = init_message.encode()
    with tempfile.NamedTemporaryFile(suffix=".ini") as tf:
        tf.write(init_message)
        tf.flush()
        subprocess.call([EDITOR, tf.name])

        tf.seek(0)
        edited_message = tf.read()
    
    has_none = False
    edited_message = edited_message.decode()
    lines = edited_message.split("\n")
    values = {}
    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith("#"):
            continue

        name, value = line.split(":")
        name = name.strip()
        value = value.strip()
        if value == "":
            value = None
            has_none = True
        values[name] = value
    
    return values, has_none


def get_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", action="store_true", help="add template")
    group.add_argument("--update", action="store_true", help="update template")
    group.add_argument("--delete", action="store_true", help="delete template")
    group.add_argument("--list", action="store_true", help="list all templates")
    group.add_argument("--instantiate", action="store_true", help="instantiate project from template")

    info_group = parser.add_argument_group("info")
    info_group.add_argument("--name", type=str, default=None, help="template name")
    info_group.add_argument("--project-dir", type=str, default=None, help="project directory for template/ project to be generated by template")
    info_group.add_argument("--template-dir", type=str, default=None, help="path to save template")
    return parser


def main():
    parser = get_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    if args.add:
        if args.name is None:
            parser._print_message("name is required", file=sys.stderr)
            return
        if args.project_dir is None:
            parser._print_message("project-dir is required", file=sys.stderr)
            return
        if args.template_dir is None:
            add_template(args.name, args.project_dir)
            print(f"add template {args.name} from {args.project_dir} to {DEFAULT_TEMPLATE_DIR}")
        else:
            add_template(args.name, args.project_dir, args.template_dir)
            print(f"add template {args.name} from {args.project_dir} to {args.template_dir}")
    elif args.update:
        if args.name is None:
            parser._print_message("name is required", file=sys.stderr)
            return
        if args.project_dir is None:
            parser._print_message("project-dir is required", file=sys.stderr)
            return
        if args.template_dir is None:
            update_template(args.name, args.project_dir)
            print(f"update template {args.name} from {args.project_dir} to {DEFAULT_TEMPLATE_DIR}")
        else:
            update_template(args.name, args.project_dir, args.template_dir)
            print(f"update template {args.name} from {args.project_dir} to {args.template_dir}")
    elif args.delete:
        if args.name is None:
            parser._print_message("name is required", file=sys.stderr)
            return
        project_dir, config = delete_template(args.name)
        print(f"delete template {args.name} from {project_dir}")
    elif args.list:
        if args.name is None:
            template_names = list_template_names()
            longest_name = max(len(name) for name in template_names)
            for name in template_names:
                project_dir, config = get_template(name)
                name = name.ljust(longest_name)
                print(f"\033[32m{name}\033[0m: \033[33m{project_dir}\033[0m")
        else:
            project_dir, config = get_template(args.name)
            print("=" * 80)
            print(f"PROJECT_DIR: {project_dir}")
            print("=" * 80)
            print(f"CONFIG_ARGS:")
            config_args = config["args"]
            for arg in config_args:
                print(f"{arg['name']}: {arg['default_value']}")
            print("=" * 80)
            print(f"STRUCTURE:")
            print_dirs_and_files(config["dirs_and_files"])
    elif args.instantiate:
        if args.name is None:
            parser._print_message("name is required", file=sys.stderr)
            return
        if args.project_dir is None:
            parser._print_message("project-dir is required", file=sys.stderr)
            return
        if os.path.exists(args.project_dir):
            parser._print_message(f"{args.project_dir} already exists", file=sys.stderr)
            return
        
        required_args = {}
        project_dir, config = get_template(args.name)
        for arg in config["args"]:
            name = arg["name"]
            default_value = arg["default_value"]
            required_args[name] = default_value

        while True:
            init_message = "# 请提供以下变量名称: \n"
            init_message += "# Please provide values for the following variables:\n"
            for name, default_value in required_args.items():
                if default_value is None:
                    init_message += f"{name}: \n"
                else:
                    init_message += f"{name}: {default_value}\n"

            required_args, has_none = get_values(init_message)
            if not has_none:
                break
            else:
                to_continue = input("变量有空值，是否继续？(y/n)")
                if to_continue == "y":
                    continue
                else:
                    sys.exit("取消操作")

        instantiate_project(args.name, args.project_dir, required_args)


if __name__ == "__main__":
    main()
