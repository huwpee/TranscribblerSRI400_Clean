# Patch for pkg_resources.declare_namespace
import sys
import types

def patch_pkg_resources_namespace():
    try:
        import pkg_resources
        
        # Check if declare_namespace is already defined
        if not hasattr(pkg_resources, 'declare_namespace'):
            # Define a simple declare_namespace function
            def declare_namespace(packageName):
                if packageName not in sys.modules:
                    sys.modules[packageName] = types.ModuleType(packageName)
                return sys.modules[packageName]
            
            # Add the function to pkg_resources
            pkg_resources.declare_namespace = declare_namespace
            print("Patched pkg_resources.declare_namespace")
    
    except Exception as e:
        print(f"Error patching pkg_resources.declare_namespace: {e}")

# Apply the patch
patch_pkg_resources_namespace()