# Patch for pkg_resources
import sys
import types

class NullProvider:
    """Null provider for resources coming from the filesystem"""
    def __init__(self, module):
        self.module = module
        self.loader = getattr(module, '__loader__', None)
    
    def get_resource_filename(self, manager, resource_name):
        return resource_name

def patch_pkg_resources():
    try:
        import pkg_resources
        if not hasattr(pkg_resources, 'NullProvider'):
            pkg_resources.NullProvider = NullProvider
            print("Patched pkg_resources.NullProvider")
    except ImportError:
        print("pkg_resources not found, skipping patch")

# Apply the patch
patch_pkg_resources()