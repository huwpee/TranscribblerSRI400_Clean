import whisper
import json
import os

def transcribe_audio(audio_path, model_size="medium", output_path=None):
    """
    Transcribe audio file using Whisper model
    
    Args:
        audio_path (str): Path to audio file
        model_size (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        output_path (str, optional): Path to save transcription JSON
        
    Returns:
        dict: Transcription result with timestamps
    """
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)
    
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(
        audio_path, 
        fp16=False, 
        language="en", 
        word_timestamps=True
    )
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Transcription saved to {output_path}")
    
    return result

if __name__ == "__main__":
    # Example usage
    audio_file = "data/sample_clip.wav"
    result = transcribe_audio(
        audio_file, 
        output_path="data/transcription.json"
    )
    
    # Print first few segments as preview
    for i, segment in enumerate(result["segments"][:2]):
        print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}")