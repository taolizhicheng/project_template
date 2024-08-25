import os

# 用于存放 template 数据库文件的目录
HOME_DIR = os.path.expanduser("~/.project-template")

# 用于存放 template 的数据库文件
DATABASE_FILE = os.path.join(HOME_DIR, "templates.json")

# 默认放置 template 的目录
DEFAULT_TEMPLATE_DIR = os.path.join(HOME_DIR, "templates")

# 使用 #{arg} 表示参数，使用 #{arg:default_value} 形式设定默认值，default_value 为默认值
ARG_REGEX = r"\#\{\w+:[\s]*[\a-zA-Z0-9\_\-\.]+\}|\#\{\w+\}"

# 模板名称规定
TEMPLATE_NAME_REGEX = r"^[a-zA-Z_]\w*$"


# 编辑器
EDITOR = os.environ.get('EDITOR', 'vim')