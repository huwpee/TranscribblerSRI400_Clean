# pkg_resources_complete_patch.py
import sys
import types
import os

# Create a minimal pkg_resources module
if 'pkg_resources' in sys.modules:
    pkg_resources = sys.modules['pkg_resources']
else:
    pkg_resources = types.ModuleType('pkg_resources')
    sys.modules['pkg_resources'] = pkg_resources

# Add basic attributes
if not hasattr(pkg_resources, '__path__'):
    pkg_resources.__path__ = []
if not hasattr(pkg_resources, '__version__'):
    pkg_resources.__version__ = '0.0.0'

# Create basic classes needed
class Distribution:
    def __init__(self, project_name='', version=''):
        self.project_name = project_name
        self.version = version
        self.key = project_name.lower() if project_name else ''
        self._provider = None
    
    def has_metadata(self, name):
        return False
    
    def get_metadata(self, name):
        return ""
    
    def requires(self):
        return []

class Requirement:
    def __init__(self, req_str=''):
        self.req_str = req_str
        self.key = req_str.lower() if req_str else ''
        
    def __str__(self):
        return self.req_str

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

class DistributionProvider:
    def __init__(self):
        pass
    
    def get_distribution(self, dist):
        return Distribution(dist)

class WorkingSet:
    def __init__(self, entries=None):
        self.entries = entries or []
        self.by_key = {}
        
    def add_entry(self, entry):
        self.entries.append(entry)
        
    def require(self, *requirements):
        return []
    
    def find(self, req):
        if req.key in self.by_key:
            return self.by_key[req.key]
        return None

    def add(self, dist, entry=None):
        if dist.key not in self.by_key:
            self.by_key[dist.key] = dist

# Add required functions and attributes
if not hasattr(pkg_resources, 'Distribution'):
    pkg_resources.Distribution = Distribution
if not hasattr(pkg_resources, 'Requirement'):
    pkg_resources.Requirement = Requirement
if not hasattr(pkg_resources, 'DistributionNotFound'):
    pkg_resources.DistributionNotFound = type('DistributionNotFound', (Exception,), {})
if not hasattr(pkg_resources, 'VersionConflict'):
    pkg_resources.VersionConflict = type('VersionConflict', (Exception,), {})
if not hasattr(pkg_resources, 'DistributionProvider'):
    pkg_resources.DistributionProvider = DistributionProvider
if not hasattr(pkg_resources, 'NullProvider'):
    pkg_resources.NullProvider = NullProvider
if not hasattr(pkg_resources, 'WorkingSet'):
    pkg_resources.WorkingSet = WorkingSet
if not hasattr(pkg_resources, 'working_set'):
    pkg_resources.working_set = WorkingSet()
if not hasattr(pkg_resources, 'Environment'):
    pkg_resources.Environment = type('Environment', (dict,), {})

# Add required functions
def require(*args, **kwargs):
    return []

def get_distribution(dist):
    return Distribution(dist)

def load_entry_point(dist, group, name):
    return None

def resource_filename(package_or_requirement, resource_name):
    return os.path.join(os.path.dirname(__file__), resource_name)

def resource_string(package_or_requirement, resource_name):
    return b""

def resource_stream(package_or_requirement, resource_name):
    return None

def resource_listdir(package_or_requirement, resource_name):
    return []

def resource_exists(package_or_requirement, resource_name):
    return False

def resource_isdir(package_or_requirement, resource_name):
    return False

def find_distributions(*args, **kwargs):
    return []

# Add functions to module if they don't exist
if not hasattr(pkg_resources, 'require'):
    pkg_resources.require = require
if not hasattr(pkg_resources, 'get_distribution'):
    pkg_resources.get_distribution = get_distribution
if not hasattr(pkg_resources, 'load_entry_point'):
    pkg_resources.load_entry_point = load_entry_point
if not hasattr(pkg_resources, 'resource_filename'):
    pkg_resources.resource_filename = resource_filename
if not hasattr(pkg_resources, 'resource_string'):
    pkg_resources.resource_string = resource_string
if not hasattr(pkg_resources, 'resource_stream'):
    pkg_resources.resource_stream = resource_stream
if not hasattr(pkg_resources, 'resource_listdir'):
    pkg_resources.resource_listdir = resource_listdir
if not hasattr(pkg_resources, 'resource_exists'):
    pkg_resources.resource_exists = resource_exists
if not hasattr(pkg_resources, 'resource_isdir'):
    pkg_resources.resource_isdir = resource_isdir
if not hasattr(pkg_resources, 'find_distributions'):
    pkg_resources.find_distributions = find_distributions

# Ensure we don't overwrite an existing module
print("pkg_resources patch applied successfully")