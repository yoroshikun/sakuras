import os
import importlib

def mount_routes(app):
    # Get the current directory
    directory = os.path.dirname(__file__)
    
    # Loop through all the files in the directory
    for filename in os.listdir(directory):
        # Ignore files that don't end with .py
        if not filename.endswith(".py"):
            continue
        
        # Import the module
        module_name = f"{__name__}.{filename[:-3]}"
        module = importlib.import_module(module_name)
        
        # Get the mount_route function and call it with the app instance
        if hasattr(module, "mount_route"):
            mount_route = getattr(module, "mount_route")
            mount_route(app)