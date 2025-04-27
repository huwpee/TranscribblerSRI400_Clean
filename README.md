# TranscribblerApp

A standalone speaker diarization and transcription application for audio and video files.

## Features

- Automatic speaker diarization (who spoke when)
- High-quality transcription using OpenAI's Whisper model
- CSV output with timestamps, speaker labels, and transcribed text
- Support for various audio and video formats
- CPU and GPU processing options

## Requirements

### IMPORTANT: FFmpeg is REQUIRED

TranscribblerApp requires FFmpeg to process audio files. You MUST install FFmpeg separately:

1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the files to a location on your computer
3. Add FFmpeg to your PATH:
   - Right-click on "This PC" or "My Computer"
   - Select "Properties"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit"
   - Click "New" and add the path to the FFmpeg bin folder
   - Click "OK" on all windows

**Quick Fix Option:** If you're having trouble with FFmpeg, download the static build from [https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip), extract it, and place the ffmpeg.exe file in the same folder as TranscribblerApp.exe.

### Hugging Face Account Setup

1. Create a Hugging Face account at [https://huggingface.co/join](https://huggingface.co/join)
2. Generate an access token at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. Accept the terms for these models (click each link and click "Accept" on the model page):
   - [pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)
   - [pyannote/segmentation](https://huggingface.co/pyannote/segmentation)

## Installation

1. Download the latest installer from [Releases](https://github.com/huwpee/TranscribblerSRI400/releases)
2. Run the installer and follow the prompts
3. Set your Hugging Face token as an environment variable:

**In PowerShell (run as administrator):**
```
[Environment]::SetEnvironmentVariable("PYANNOTE_AUTH_TOKEN", "your_token_here", "Machine")
```

**In Command Prompt (run as administrator):**
```
setx PYANNOTE_AUTH_TOKEN "your_token_here" /M
```

To run PowerShell as administrator:
1. Search for "PowerShell" in the Start menu
2. Right-click on "Windows PowerShell" and select "Run as administrator"

## Usage

### Basic Usage

```
TranscribblerApp.exe --input "path\to\audio.wav" --output "path\to\output.csv" --whisper-model base.en --device cpu --pyannote-token %PYANNOTE_AUTH_TOKEN%
```

### Command Line Options

- `--input`: Path to input audio/video file (required)
- `--output`: Path to output CSV file (required)
- `--whisper-model`: Whisper model to use (default: base.en)
- `--device`: Device to use for processing (cpu or cuda)
- `--pyannote-token`: Hugging Face token for pyannote models

## Troubleshooting

### Application Won't Start

1. Verify FFmpeg is installed and in your PATH
2. Check that your Hugging Face token is set correctly
3. Ensure you've accepted the terms for both pyannote models
4. Try running the application from Command Prompt to see error messages

### Installation Issues

If the installer won't run after downloading:
1. Right-click the installer and select "Properties"
2. Check for an "Unblock" option at the bottom and click it
3. Click "Apply" and try running the installer again

If you previously installed the application and are having issues reinstalling:
1. Clean up the PATH environment variable (see Requirements section)
2. Remove any leftover files from the previous installation
3. Reboot your computer before attempting to reinstall

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for transcription
- [Pyannote Audio](https://github.com/pyannote/pyannote-audio) for speaker diarization
- [FFmpeg](https://ffmpeg.org/) for audio processing
