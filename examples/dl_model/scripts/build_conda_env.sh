#! /bin/bash

# 检测conda是否安装
if ! command -v conda &> /dev/null
then
    echo "conda could not be found, please install it first."
    exit 1
fi

# 创建conda环境
if conda env list | awk -F' ' '{print $1}' | grep -q #{env_name}
then
    echo "Environment #{env_name:paper} already exists."
    exit 1
fi

conda create -n #{env_name} python=#{python_version:3.10}

# 安装依赖
THIS_SCRIPT_DIR=$(dirname $(readlink -f "$0"))
PROJECT_DIR=$(dirname $THIS_SCRIPT_DIR)
