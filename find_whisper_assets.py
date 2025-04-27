# save this as find_whisper_assets.py
import whisper
import os
import shutil

# Print the location of the whisper package
print(whisper.__file__)

# Get the assets directory
assets_dir = os.path.join(os.path.dirname(whisper.__file__), "assets")
print(f"Assets directory: {assets_dir}")

# Create the whisper_assets directory in your project
os.makedirs("whisper_assets", exist_ok=True)

# Copy the mel_filters.npz file
shutil.copy(os.path.join(assets_dir, "mel_filters.npz"), "whisper_assets")
print("File copied successfully!")