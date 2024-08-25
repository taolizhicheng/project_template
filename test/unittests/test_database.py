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

from project_template.database import add_template, delete_template, update_template, get_template, list_template_names
from project_template.util import save_read_json
from project_template.constants import DATABASE_FILE, DEFAULT_TEMPLATE_DIR


class TestAddTemplate(unittest.TestCase):
    def test_add_template(self):
        name = "test_template"
        project_dir = os.path.join(MODULE_DIR, "examples", "dl_model")
        add_template(name, project_dir)

        database = save_read_json(DATABASE_FILE)
        self.assertIn(name, database)
        
        template = database[name]
        self.assertEqual(template["project_dir"], project_dir)
        self.assertEqual(template["location"], DEFAULT_TEMPLATE_DIR)
        self.assertEqual(template["config_file"], f"{DEFAULT_TEMPLATE_DIR}/{name}.json")
        self.assertTrue(os.path.exists(template["config_file"]))

        config = save_read_json(template["config_file"])
        self.assertIn("dirs_and_files", config)
        self.assertIn("args", config)
        
        args = config["args"]
        args_keys = [arg["name"] for arg in args]
        self.assertListEqual(args_keys, ["env_name", "model", "python_version", "MODEL"])
        
        self.assertRaises(ValueError, add_template, name, project_dir)
        self.assertRaises(ValueError, add_template, name, f"{project_dir}/not_a_dir")
        self.assertRaises(ValueError, add_template, name, f"{project_dir}/README.md")
        self.assertRaises(ValueError, add_template, name, project_dir)
        try:
            delete_template(name)
        except Exception as e:
            self.fail(f"delete_template failed: {e}")
    
    def test_add_template_with_location(self):
        name = "test_template"
        project_dir = os.path.join(MODULE_DIR, "examples", "dl_model")
        location_dir = os.path.join("/tmp/templates")
        add_template(name, project_dir, location_dir)

        database = save_read_json(DATABASE_FILE)
        self.assertIn(name, database)

        template = database[name]
        self.assertEqual(template["location"], location_dir)
        self.assertEqual(template["config_file"], f"{location_dir}/{name}.json")
        self.assertTrue(os.path.exists(template["config_file"]))

        config = save_read_json(template["config_file"])
        self.assertIn("dirs_and_files", config)
        self.assertIn("args", config)
        
        args = config["args"]
        args_keys = [arg["name"] for arg in args]
        self.assertListEqual(args_keys, ["env_name", "model", "python_version", "MODEL"])

        try:
            delete_template(name)
        except Exception as e:
            self.fail(f"delete_template failed: {e}")


class TestDeleteTemplate(unittest.TestCase):
    def test_delete_template(self):
        name = "test_template"
        self.assertRaises(ValueError, delete_template, name)

        project_dir = os.path.join(MODULE_DIR, "examples", "dl_model")
        add_template(name, project_dir)

        deleted_project_dir, deleted_config = delete_template(name)
        self.assertEqual(deleted_project_dir, project_dir)

        database = save_read_json(DATABASE_FILE)
        self.assertNotIn(name, database)

        location_dir = f"{DEFAULT_TEMPLATE_DIR}/{name}.json"
        self.assertFalse(os.path.exists(location_dir))


class TestUpdateTemplate(unittest.TestCase):
    def test_update_template(self):
        name = "test_template"
        project_dir = os.path.join(MODULE_DIR, "examples", "dl_model")
        self.assertRaises(ValueError, update_template, name, project_dir)

        add_template(name, project_dir)

        update_template(name, project_dir)

        database = save_read_json(DATABASE_FILE)
        self.assertIn(name, database)

        template = database[name]
        self.assertEqual(template["project_dir"], project_dir)
        self.assertEqual(template["location"], DEFAULT_TEMPLATE_DIR)
        self.assertEqual(template["config_file"], f"{DEFAULT_TEMPLATE_DIR}/{name}.json")

        config = save_read_json(template["config_file"])
        self.assertIn("dirs_and_files", config)
        self.assertIn("args", config)
        
        args = config["args"]
        args_keys = [arg["name"] for arg in args]
        self.assertListEqual(args_keys, ["env_name", "model", "python_version", "MODEL"])

        delete_template(name)


class TestGetTemplate(unittest.TestCase):
    def test_get_template(self):
        name = "test_template"
        project_dir = os.path.join(MODULE_DIR, "examples", "dl_model")
        add_template(name, project_dir)

        project_dir_from_db, config = get_template(name)
        self.assertEqual(project_dir_from_db, project_dir)

        self.assertIn("dirs_and_files", config)
        self.assertIn("args", config)
        
        args = config["args"]
        args_keys = [arg["name"] for arg in args]
        self.assertListEqual(args_keys, ["env_name", "model", "python_version", "MODEL"])

        delete_template(name)


class TestListTemplateNames(unittest.TestCase):
    def test_list_template_names(self):
        name = "test_template"
        project_dir = os.path.join(MODULE_DIR, "examples", "dl_model")
        add_template(name, project_dir)

        names = list_template_names()
        self.assertIn(name, names)

        delete_template(name)


if __name__ == "__main__":
    unittest.main()
