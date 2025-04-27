import whisper, os

# Download or load the model into cache
model = whisper.load_model("medium.en")

# Whisper’s default cache path
cache_root = whisper._MODELS_PATH if hasattr(whisper, "_MODELS_PATH") \
             else os.path.expanduser("~/.cache/whisper/models")

print("Model lives at:", cache_root)