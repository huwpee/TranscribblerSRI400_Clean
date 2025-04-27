# Add NullProvider if it doesn't exist
if not hasattr(pkg_resources, 'NullProvider'):
    class NullProvider:
        def __init__(self, *args, **kwargs):
            pass
            
        def has_metadata(self, name):
            return False
            
        def get_metadata(self, name):
            return ""
            
        def get_resource_filename(self, manager, resource_name):
            return ""
            
        def get_resource_stream(self, manager, resource_name):
            return None
            
        def get_resource_string(self, manager, resource_name):
            return b""
            
        def has_resource(self, resource_name):
            return False
            
        def resource_isdir(self, resource_name):
            return False
            
        def resource_listdir(self, resource_name):
            return []
    
    pkg_resources.NullProvider = NullProvider
    print("Added NullProvider to pkg_resources in PyInstaller hook")