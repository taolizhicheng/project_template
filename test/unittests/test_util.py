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
from project_template.util import save_write_json, save_read_json, is_directory_empty, scan_args_for_string, format_string


class TestUtil(unittest.TestCase):
    def test_save_write_json(self):
        json_result = {"test": "test"}
        json_path = "/tmp/test.json"
        save_write_json(json_path, json_result)
        self.assertTrue(os.path.exists(json_path))
        self.assertDictEqual(json_result, save_read_json(json_path))

    def test_save_read_json(self):
        json_result = {"test": "test"}
        json_path = "/tmp/test.json"
        save_write_json(json_path, json_result)
        self.assertDictEqual(json_result, save_read_json(json_path))

    def test_is_directory_empty(self):
        os.makedirs("/tmp/test")
        self.assertTrue(is_directory_empty("/tmp/test"))
        os.makedirs("/tmp/test/test")
        self.assertFalse(is_directory_empty("/tmp/test"))
        shutil.rmtree("/tmp/test")

    def test_scan_args_for_string(self):
        string = "#{a:1}, #{b:2}, #{c}"
        args = scan_args_for_string(string)
        self.assertListEqual(args, [{"name": "a", "default_value": "1"}, {"name": "b", "default_value": "2"}, {"name": "c", "default_value": None}])

    def test_format_string(self):
        string = "#{a:1}, #{b:2}, #{c}"
        args = {"a": "1", "b": "2", "c": "3"}
        formatted_string = format_string(string, args)
        self.assertEqual(formatted_string, "1, 2, 3")