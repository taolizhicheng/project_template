import os
import sys
import unittest


sys.dont_write_bytecode = True

MODULE_DIR = os.environ.get('MODULE_DIR', None)
if MODULE_DIR is not None:
    if MODULE_DIR not in sys.path:
        sys.path = [MODULE_DIR] + sys.path
else:
    raise ValueError("TEMPLATE_PROJECT_DIR environment variable not set!")


import shutil
from project_template.database import add_template, delete_template
from project_template.instantiation import instantiate_project


class TestInstantiation(unittest.TestCase):
    def test_instantiate_project(self):
        name = "test_template"
        project_dir = f"{MODULE_DIR}/examples/dl_model"
        add_template(name, project_dir)

        project_dir = f"/tmp/{name}"
        args = {
            "env_name": "test_env",
            "model": "ssd",
            "python_version": "3.10",
            "MODEL": "SSD",
        }
        instantiate_project(name, project_dir, args)

        delete_template(name)

        self.assertTrue(os.path.exists(project_dir))
        # 检测ssd目录结构
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "dataset")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "dataset", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "model")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "model", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "model", "ssd.py")))
        with open(os.path.join(project_dir, "ssd", "model", "ssd.py"), "r") as f:
            content = f.read()
            gt = "import torch\n" \
                 "import torch.nn as nn\n" \
                 "import torch.nn.functional as F\n" \
                 "\n\n\n" \
                 "class SSD(nn.Module):\n" \
                 "    def __init__(self, *args, **kwargs):\n" \
                 "        super().__init__(*args, **kwargs)\n" \
                 "    \n" \
                 "    def forward(self, x):\n" \
                 "        pass\n"
            self.assertEqual(content, gt)

        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "scheduler")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "scheduler", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "trainer")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "ssd", "trainer", "__init__.py")))


        self.assertTrue(os.path.exists(os.path.join(project_dir, "assets")))

        self.assertTrue(os.path.exists(os.path.join(project_dir, "data")))

        self.assertTrue(os.path.exists(os.path.join(project_dir, "docs")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "docs", "notebooks")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "docs", "notebooks", "exam.ipynb")))

        self.assertTrue(os.path.exists(os.path.join(project_dir, "scripts")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "scripts", "build_conda_env.sh")))
        with open(os.path.join(project_dir, "scripts", "build_conda_env.sh"), "r") as f:
            content = f.read()
            gt = '#! /bin/bash\n\n# 检测conda是否安装\n' + \
                 'if ! command -v conda &> /dev/null\nthen\n' + \
                 '    echo "conda could not be found, please install it first."\n' + \
                 '    exit 1\nfi\n\n# 创建conda环境\nif conda env list | awk -F\' \' \'{print $1}\' | grep -q test_env\nthen\n' + \
                 '    echo "Environment test_env already exists."\n' + \
                 '    exit 1\nfi\n\nconda create -n test_env python=3.10\n\n' + \
                 '# 安装依赖\nTHIS_SCRIPT_DIR=$(dirname $(readlink -f "$0"))\nPROJECT_DIR=$(dirname $THIS_SCRIPT_DIR)\n'
            self.assertEqual(content, gt)
            
        self.assertTrue(os.path.exists(os.path.join(project_dir, "scripts", "download_data.sh")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "scripts", "inference.sh")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "scripts", "train.sh")))

        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "ssd")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "ssd", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "ssd", "test_ssd.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "dataset")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "dataset", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "scheduler")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "scheduler", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "trainer")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "tests", "unittests", "trainer", "__init__.py")))

        self.assertTrue(os.path.exists(os.path.join(project_dir, "README.md")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "requirements.txt")))

        shutil.rmtree(project_dir)


if __name__ == "__main__":
    unittest.main()