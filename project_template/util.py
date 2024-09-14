import os
import re
import json
import fcntl
import fnmatch

from project_template.constants import ARG_REGEX


__all__ = [
    "save_write_json", "save_read_json", "is_directory_empty", "scan_args_for_string", "format_string"
]


def save_write_json(file_path, content):
    """
    @brief  将json内容写入文件，并确保写入操作是原子的

    @param file_path    文件路径
    @param content      要写入的内容
    """
    with open(file_path, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            json.dump(content, f, indent=4, ensure_ascii=False)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def save_read_json(file_path):
    """
    @brief  从文件中读取json内容

    @param file_path 文件路径
    @return 文件中的json内容
    """
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            return json.load(f)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def is_directory_empty(directory):
    """
    @brief  判断目录是否为空

    @param directory 目录路径
    @return 目录是否为空
    """
    return len(os.listdir(directory)) == 0



def scan_args_for_string(string: str):
    """
    @brief  扫描字符串中的参数
    @detail 扫描字符串中满足 #{name:default_value} 模式的参数，并返回对应的参数列表

    @param  string 要扫描的字符串
    @return 包含参数名称和默认值的列表
    """
    matches = re.finditer(ARG_REGEX, string)
    args = []

    for match_ in matches:
        start, end = match_.span()
        arg_name = match_.group()[2:-1]
        if ":" in arg_name:
            arg_name, default_value = arg_name.split(":")
        else:
            default_value = None
        
        args.append({
            "name": arg_name,
            "default_value": default_value,
        })
    return args


def format_string(string: str, args: dict):
    """
    @brief  格式化字符串
    @detail 将字符串中的参数替换为对应的值

    @param  string 要格式化的字符串
    @param  args 参数列表
    @return 格式化后的字符串
    """
    replace_intervals = []
    matches = re.finditer(ARG_REGEX, string)
    for match_ in matches:
        start, end = match_.span()
        arg_name = match_.group()[2:-1]
        if ":" in arg_name:
            arg_name, _ = arg_name.split(":")

        value = args[arg_name]
        value = str(value)

        replace_intervals.append((start, end, value))
    
    if len(replace_intervals) == 0:
        return string
    
    start = 0
    end = replace_intervals[0][0]
    final_string = string[start:end]

    for i in range(len(replace_intervals) - 1):
        start, end, value = replace_intervals[i]
        final_string += value

        start = end
        end = replace_intervals[i+1][0]
        final_string += string[start:end]

    start, end, value = replace_intervals[-1]
    final_string += value
    final_string += string[end:]

    return final_string


def whether_ignore_file(file_path: str, ignore_pattern: str):
    """
    @brief  判断文件是否需要忽略
    @detail 判断文件是否需要忽略，使用 fnmatch 进行匹配

    @param  file_path 文件路径
    @param  ignore_pattern 忽略模式
    @return 是否需要忽略
    """
    full_pattern = "*/" + ignore_pattern
    if ignore_pattern.endswith("/"):
        full_pattern += "*"
    to_ignore1 = fnmatch.fnmatch(file_path, full_pattern)
    
    full_pattern = "*/" + ignore_pattern
    full_pattern = full_pattern.rstrip("/")
    to_ignore2 = fnmatch.fnmatch(file_path, full_pattern)

    return to_ignore1 or to_ignore2
