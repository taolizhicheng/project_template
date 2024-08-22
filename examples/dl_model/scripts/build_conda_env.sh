#! /bin/bash

# 检测conda是否安装
if ! command -v conda &> /dev/null
then
    echo "conda could not be found, please install it first."
    exit 1
fi

# 创建conda环境
conda create -n #{env_name} python=#{python_version:3.10}

# 安装依赖
THIS_SCRIPT_DIR=$(dirname $(readlink -f "$0"))
PROJECT_DIR=$(dirname $THIS_SCRIPT_DIR)
