#!/usr/bin/env python3
"""
diarize.py: defines diarize_audio() to perform speaker diarization using pyannote.audio.
"""

import os
import logging
import numpy as np

# Patch for NumPy 2.0 compatibility
if not hasattr(np, 'NaN'):
    np.NaN = float("nan")
    print("Patched np.NaN for NumPy 2.0 compatibility in diarize.py")

try:
    from pyannote.audio import Pipeline
except ImportError:
    raise ImportError("pyannote.audio is required. Install with: pip install pyannote.audio")

def diarize_audio(audio_path: str,
                  auth_token: str,
                  pipeline_name: str = "pyannote/speaker-diarization"):
    """
    Perform speaker diarization on the given audio file.
    Returns a pyannote.core.Annotation with speaker turns.
    """
    logging.info(f"Loading diarization pipeline '{pipeline_name}'")
    pipeline = Pipeline.from_pretrained(pipeline_name,
                                       use_auth_token=auth_token)
    return pipeline({"uri": os.path.basename(audio_path),
                     "audio": audio_path})

def main():
    import configargparse
    parser = configargparse.ArgumentParser(
        description="Run speaker diarization on an audio file.",
        default_config_files=['config.ini'],
        ignore_unknown_config_file_keys=True
    )
    parser.add_argument(
        '-i', '--input',
        dest='input_audio',
        required=True,
        help='Path to input audio file'
    )
    parser.add_argument(
        '--pyannote-token',
        env_var='PYANNOTE_AUTH_TOKEN',
        dest='auth_token',
        required=True,
        help='Hugging Face token for pyannote.audio'
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input_audio):
        logging.error(f"Input audio not found: {args.input_audio}")
        exit(1)

    annotation = diarize_audio(
        audio_path=args.input_audio,
        auth_token=args.auth_token
    )

    # Print out speaker turns: start, end, speaker label
    for turn, _, speaker in annotation.itertracks(yield_label=True):
        print(f"{turn.start:.2f}\t{turn.end:.2f}\t{speaker}")

if __name__ == '__main__':
    main()