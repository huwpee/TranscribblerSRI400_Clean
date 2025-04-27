# altgraph_patch.py
import sys
import types

# Create a fake altgraph module
altgraph_module = types.ModuleType('altgraph')
altgraph_module.__version__ = '0.17.3'  # Use the version you have installed

# Create fake submodules that pkg_resources might try to access
altgraph_module.ObjectGraph = types.ModuleType('altgraph.ObjectGraph')
altgraph_module.Graph = types.ModuleType('altgraph.Graph')
altgraph_module.GraphUtil = types.ModuleType('altgraph.GraphUtil')
altgraph_module.GraphAlgo = types.ModuleType('altgraph.GraphAlgo')

# Register the modules in sys.modules
sys.modules['altgraph'] = altgraph_module
sys.modules['altgraph.ObjectGraph'] = altgraph_module.ObjectGraph
sys.modules['altgraph.Graph'] = altgraph_module.Graph
sys.modules['altgraph.GraphUtil'] = altgraph_module.GraphUtil
sys.modules['altgraph.GraphAlgo'] = altgraph_module.GraphAlgo

# Patch pkg_resources to avoid checking for altgraph
try:
    import pkg_resources
    original_require = pkg_resources.require
    
    def patched_require(*args, **kwargs):
        try:
            return original_require(*args, **kwargs)
        except pkg_resources.DistributionNotFound as e:
            if 'altgraph' in str(e):
                return []
            raise
    
    pkg_resources.require = patched_require
except ImportError:
    pass