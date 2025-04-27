
# Runtime hook
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])
logger = logging.getLogger('TranscribblerApp')

logger.debug("Starting runtime hook")

# Add bundle directory to path
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
logger.debug(f"Bundle directory: {bundle_dir}")
sys.path.insert(0, bundle_dir)

# Set environment variables
os.environ['PYTHONPATH'] = bundle_dir
os.environ['PATH'] = os.path.join(bundle_dir, 'bin') + os.pathsep + os.environ.get('PATH', '')
logger.debug("Environment variables set")

# Fix NumPy compatibility issues
logger.debug("Fixing NumPy compatibility")
import numpy as np
if not hasattr(np, 'float'):
    np.float = float
if not hasattr(np, 'int'):
    np.int = int
if not hasattr(np, 'bool'):
    np.bool = bool
if not hasattr(np, 'object'):
    np.object = object
if not hasattr(np, 'NaN'):
    np.NaN = float('nan')

logger.debug("Runtime hook completed")
