#!/usr/bin/env python3
"""
TranscribblerApp: A CLI tool that transcribes an audio/video file with OpenAI Whisper,
performs speaker diarization via diarize.py, then writes a CSV of
timestamped, speaker‑labelled segments.
"""

import configargparse as argparse
import csv
import logging
import os
import sys
import subprocess
from pathlib import Path

# FFmpeg locator function to find ffmpeg in various locations
def find_ffmpeg():
    """
    Find ffmpeg executable in multiple possible locations:
    1. In the same directory as the application
    2. In a 'bin' subdirectory
    3. In the installation directory (C:\Program Files (x86)\TranscribblerApp\)
    4. In the system PATH
    """
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        app_dir = Path(os.path.dirname(sys.executable))
    else:
        app_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Possible locations to check
    possible_locations = [
        app_dir / "ffmpeg.exe",
        app_dir / "bin" / "ffmpeg.exe",
        Path(r"C:\Program Files (x86)\TranscribblerApp\ffmpeg.exe"),
        Path(r"C:\Program Files\TranscribblerApp\ffmpeg.exe")
    ]
    
    # Check each location
    for location in possible_locations:
        if location.exists():
            logging.info(f"Found FFmpeg at: {location}")
            return str(location)
    
    # If not found in specific locations, try to find in PATH
    try:
        result = subprocess.run(["where", "ffmpeg"], 
                               capture_output=True, 
                               text=True, 
                               check=False)
        if result.returncode == 0 and result.stdout.strip():
            ffmpeg_path = result.stdout.strip().split('\n')[0]
            logging.info(f"Found FFmpeg in PATH: {ffmpeg_path}")
            return ffmpeg_path
    except Exception as e:
        logging.warning(f"Error checking FFmpeg in PATH: {e}")
    
    logging.error("FFmpeg not found. Please install FFmpeg and place it in the application directory.")
    return None

# Configure environment for FFmpeg
def configure_ffmpeg():
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        logging.error("FFmpeg not found. Please install FFmpeg according to the README instructions.")
        logging.error("Place ffmpeg.exe in C:\\Program Files (x86)\\TranscribblerApp\\")
        sys.exit(1)
    
    # Set environment variable for libraries that use FFmpeg
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    
    # For Whisper specifically
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    
    return ffmpeg_path

try:
    import whisper
except ImportError:
    print("Error: please install OpenAI Whisper (pip install openai-whisper)")
    sys.exit(1)

from diarize import diarize_audio

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

def parse_args():
    parser = argparse.ArgumentParser(
        description="Transcribe and diarize audio/video into a speaker‑labelled CSV.",
        default_config_files=['config.ini'],
        ignore_unknown_config_file_keys=True
    )
    parser.add_argument('-c', '--config',
                        is_config_file=True,
                        help='Path to config file (INI or YAML)')
    parser.add_argument('-i', '--input',
                        required=True,
                        help='Path to input audio or video file')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='Path to output CSV file (overwritten if exists)')
    parser.add_argument('--whisper-model',
                        default='base',
                        choices=whisper.available_models(),
                        help='Whisper model size (tiny, base, small, medium, large)')
    parser.add_argument('--device',
                        default='cpu',
                        choices=['cpu', 'cuda'],
                        help='Device for Whisper inference')
    parser.add_argument('--pyannote-token',
                        env_var='PYANNOTE_AUTH_TOKEN',
                        required=True,
                        help='Hugging Face token for pyannote.audio')
    return parser.parse_args()

def transcribe_audio(model, input_path: str):
    logging.info(f"Transcribing {input_path} with Whisper...")
    result = model.transcribe(input_path, word_timestamps=False)
    segments = result.get("segments", [])
    if not segments:
        logging.warning("No segments returned by Whisper.")
    return segments

def align_and_write_csv(segments, turns, output_path: str):
    logging.info(f"Writing aligned transcript to {output_path}...")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["start", "end", "speaker", "text"])
        for seg in segments:
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()
            midpoint = (start + end) / 2.0
            assigned = "unknown"
            for turn_start, turn_end, speaker in turns:
                if turn_start <= midpoint <= turn_end:
                    assigned = speaker
                    break
            writer.writerow([f"{start:.2f}", f"{end:.2f}", assigned, text])
    logging.info("CSV writing complete.")

def main():
    setup_logger()
    
    # Configure FFmpeg before anything else
    ffmpeg_path = configure_ffmpeg()
    logging.info(f"Using FFmpeg from: {ffmpeg_path}")
    
    args = parse_args()

    if not os.path.isfile(args.input):
        logging.error(f"Input file not found: {args.input}")
        sys.exit(1)

    # 1) Load Whisper and transcribe
    logging.info(f"Loading Whisper '{args.whisper_model}' on {args.device}...")
    whisper_model = whisper.load_model(args.whisper_model, device=args.device)
    segments = transcribe_audio(whisper_model, args.input)

    # 2) Run speaker diarization
    try:
        annotation = diarize_audio(audio_path=args.input, auth_token=args.pyannote_token)
        turns = [
            (segment.start, segment.end, speaker)
            for segment, _, speaker in annotation.itertracks(yield_label=True)
        ]
    except Exception as e:
        logging.error(f"Diarization failed: {e}")
        sys.exit(1)

    # 3) Align segments to speaker turns and write CSV
    try:
        align_and_write_csv(segments, turns, args.output)
    except Exception as e:
        logging.error(f"Failed to write CSV: {e}")
        sys.exit(1)

    logging.info("TranscribblerApp finished successfully.")

if __name__ == "__main__":
    main()