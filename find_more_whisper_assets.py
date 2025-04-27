import whisper
import os
import shutil

# Get the assets directory
assets_dir = os.path.join(os.path.dirname(whisper.__file__), "assets")
print(f"Assets directory: {assets_dir}")

# List all files in the assets directory
print("Files in assets directory:")
for file in os.listdir(assets_dir):
    print(f" - {file}")
    # Copy all files to whisper_assets directory
    source = os.path.join(assets_dir, file)
    destination = os.path.join("whisper_assets", file)
    shutil.copy(source, destination)
    print(f"Copied {file}")

print("All files copied successfully!")