
import os
import sys
import site
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])
logger = logging.getLogger('TranscribblerApp')

try:
    logger.debug("Starting bootstrap")
    
    # Add directories to sys.path
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    logger.debug(f"Bundle directory: {bundle_dir}")
    sys.path.insert(0, bundle_dir)
    site.addsitedir(bundle_dir)
    
    # Set environment variables
    os.environ['PYTHONPATH'] = bundle_dir
    os.environ['PATH'] = os.path.join(bundle_dir, 'bin') + os.pathsep + os.environ.get('PATH', '')
    
    # Import and run the main application
    logger.debug("Importing Main module")
    import Main
    
    if __name__ == '__main__':
        logger.debug(f"Command line arguments: {sys.argv}")
        if len(sys.argv) > 1:
            logger.debug(f"Processing video: {sys.argv[1]}")
            Main.process_video(sys.argv[1])
        else:
            logger.debug("No arguments provided, showing usage")
            Main.print_usage()
            
except Exception as e:
    logger.error(f"Error in bootstrap: {e}")
    logger.error(traceback.format_exc())
    print(f"ERROR: {e}")
    print(traceback.format_exc())
    input("Press Enter to exit...")
    sys.exit(1)
