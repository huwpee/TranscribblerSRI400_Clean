import subprocess
import os
import sys
import shutil # Used for shutil.which to find ffmpeg in PATH

# Helper function to find resources when bundled by PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # Correct attribute is _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Fallback for normal execution (running as a script)
        base_path = os.path.abspath(".") 
    except Exception as e:
        # Catch any other unexpected errors during path resolution
        print(f"Warning: Error determining base path: {e}")
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to locate the FFmpeg executable
def find_ffmpeg_executable(ffmpeg_path_override=None):
    """
    Finds the FFmpeg executable path in a specific order:
    1. User-provided override path.
    2. Bundled executable (in 'bin' folder relative to script/bundle).
    3. System PATH.
    
    Args:
        ffmpeg_path_override (str, optional): Path provided via command line or config.
        
    Returns:
        str: The path to the found FFmpeg executable, or None if not found.
    """
    # 1. Check override path from command line/config
    if ffmpeg_path_override:
        # Check if the override path actually exists and is a file
        if os.path.isfile(ffmpeg_path_override):
             print(f"Using FFmpeg from override path: {ffmpeg_path_override}")
             return ffmpeg_path_override
        else:
             print(f"Warning: Override FFmpeg path specified but not found: {ffmpeg_path_override}")
            
    # 2. Check for bundled executable relative to script/bundle
    # Determine expected executable name based on OS
    ffmpeg_exe_name = 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg' 
    # Construct path relative to the base path (script dir or _MEIPASS)
    bundled_ffmpeg_path = resource_path(os.path.join('bin', ffmpeg_exe_name))
    
    if os.path.isfile(bundled_ffmpeg_path):
        print(f"Using bundled FFmpeg: {bundled_ffmpeg_path}")
        return bundled_ffmpeg_path
            
    # 3. Check system PATH using shutil.which (more robust than just checking PATH env var)
    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        print(f"Using FFmpeg from system PATH: {ffmpeg_in_path}")
        return ffmpeg_in_path

    # 4. Not found anywhere
    print("Error: FFmpeg executable not found.")
    print("Please ensure FFmpeg is installed and in your system PATH,")
    print("or specify its location using the --ffmpeg argument in the command line,")
    print("or place the executable in a 'bin' subfolder next to the script/application.")
    return None

# Main function to extract audio using the located FFmpeg
def extract_audio(video_path, output_path, sample_rate=16000, ffmpeg_path_override=None):
    """
    Extract audio from video file and save as WAV using the located FFmpeg.
    
    Args:
        video_path (str): Path to input video file.
        output_path (str): Path to save extracted audio WAV file.
        sample_rate (int): Sample rate for extracted audio. Defaults to 16000.
        ffmpeg_path_override (str, optional): User-specified path to FFmpeg.
        
    Returns:
        str: Path to the extracted audio file if successful, otherwise None.
    """
    
    # Find the appropriate FFmpeg executable to use
    ffmpeg_exec = find_ffmpeg_executable(ffmpeg_path_override)
    
    # If FFmpeg was not found, raise an error to stop processing
    if not ffmpeg_exec:
        raise FileNotFoundError("FFmpeg executable could not be located. Cannot extract audio.")
            
    print(f"Extracting audio using FFmpeg command:")
    # Construct the command arguments list
    command = [
        ffmpeg_exec, 
        "-i", video_path,       # Input file
        "-vn",                  # Disable video recording
        "-acodec", "pcm_s16le", # Audio codec: PCM signed 16-bit little-endian (standard WAV)
        "-ac", "1",             # Number of audio channels: 1 (mono)
        "-ar", str(sample_rate),# Audio sample rate
        output_path,            # Output file path
        "-y"                    # Overwrite output file if it exists
    ]
    print(f"Running command: {' '.join(command)}") # Print the command for debugging
    
    try:
        # Execute the FFmpeg command
        result = subprocess.run(
            command, 
            check=True, # Raise CalledProcessError if FFmpeg returns a non-zero exit code
            stdout=subprocess.PIPE, # Capture standard output
            stderr=subprocess.PIPE, # Capture standard error
            encoding='utf-8'        # Decode stdout/stderr as text
        )
        print(f"FFmpeg stdout:\n{result.stdout}") # Print FFmpeg output for info
        print(f"Audio extracted successfully to {output_path}")
        return output_path
        
    except FileNotFoundError:
        # This might happen if ffmpeg_exec path is somehow invalid despite checks
        print(f"Error: The FFmpeg executable path seems invalid: {ffmpeg_exec}")
        return None
    except subprocess.CalledProcessError as e:
        # This catches errors reported by FFmpeg itself (non-zero exit code)
        print(f"Error during FFmpeg execution (return code {e.returncode}):")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"FFmpeg stderr:\n{e.stderr}") # Print FFmpeg's error message
        return None
    except Exception as e:
        # Catch any other unexpected exceptions during subprocess execution
        print(f"An unexpected error occurred during audio extraction: {e}")
        return None

# Example usage block (optional, usually removed or commented out for bundled apps)
# if __name__ == "__main__":
#     print("Testing audio extraction...")
#     # Create dummy files/folders for testing if needed
#     if not os.path.exists("test_output"):
#         os.makedirs("test_output")
#     # Replace with a real video file path for actual testing
#     test_video = "path/to/your/test_video.mp4" 
#     test_output = "test_output/extracted_audio.wav"
#     
#     if os.path.exists(test_video):
#         extracted_file = extract_audio(test_video, test_output)
#         if extracted_file:
#             print(f"Test successful: Audio saved to {extracted_file}")
#         else:
#             print("Test failed: Audio extraction returned None.")
#     else:
#         print(f"Test video not found at: {test_video}. Skipping test.")
