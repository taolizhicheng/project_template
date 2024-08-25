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



from project_template.scan import scan_directory, scan_args


class TestScan(unittest.TestCase):
    def test_scan_directory(self):
        project_dir = f"{MODULE_DIR}/examples/dl_model"
        dirs_and_files = scan_directory(project_dir)
        
        for dir_or_file in dirs_and_files:
            name = dir_or_file["name"]
            type_ = dir_or_file["type"]
            root = dir_or_file["root"]
            mode = dir_or_file["mode"]
            content = dir_or_file["content"]
            path = os.path.join(project_dir, root, name)
            if type_ == "file":
                self.assertTrue(os.path.exists(path))
                self.assertTrue(os.path.isfile(path))
            elif type_ == "dir":
                self.assertTrue(os.path.exists(path))
                self.assertTrue(os.path.isdir(path))


class TestScanArgs(unittest.TestCase):
    def test_scan_args(self):
        project_dir = f"{MODULE_DIR}/examples/dl_model"
        dirs_and_files = scan_directory(project_dir)
        args = scan_args(dirs_and_files)
        
        gt = [
            {
                "name": "env_name",
                "default_value": "paper",
            },
            {
                "name": "model",
                "default_value": None,
            },
            {
                "name": "python_version",
                "default_value": "3.10",
            },
            {
                "name": "MODEL",
                "default_value": None,
            },
        ]
        self.assertListEqual(args, gt)


if __name__ == "__main__":
    unittest.main()
