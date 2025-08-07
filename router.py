# router.py
import importlib.util
import sys
import os

class Router:
    def __init__(self):
        self.default_controller = "home"
        self.default_action = "index"

    def route(self, path):
        parts = path.strip("/").split("/")
        controller_name = parts[0] if parts[0] else self.default_controller
        action_name = parts[1] if len(parts) > 1 else self.default_action
        params = parts[2:] if len(parts) > 2 else []

        controller_file = f"Frontend/Controllers/{controller_name}_controller.py"
        class_name = f"{controller_name.capitalize()}Controller"

        if not os.path.isfile(controller_file):
            return f"Error: Page '{controller_file}' not found"

        spec = importlib.util.spec_from_file_location(class_name, controller_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[class_name] = module
        spec.loader.exec_module(module) 

        controller_class = getattr(module, class_name, None)
        if controller_class is None:
            return f"Error: Class '{class_name}' not found in {controller_file}"

        controller_instance = controller_class()

        if not hasattr(controller_instance, action_name):
            return f"Error: Method '{action_name}' not found in {class_name}"

        return getattr(controller_instance, action_name)(*params)
