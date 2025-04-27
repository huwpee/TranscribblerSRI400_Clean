# README.md

TranscribblerApp is a Windows command‑line tool that performs speech‑to‑text transcription using OpenAI’s Whisper and speaker diarisation with Pyannote. It ships as a single, standalone installer that bundles Python, Whisper, Pyannote, all necessary patches and hooks, plus the FFmpeg executable. End users need only run the installer—no additional dependency installation is required.

Installation  
Download `TranscribblerAppInstaller-1.0.0.exe` from the project’s GitHub Releases page and launch it with administrator privileges. By default, TranscribblerApp installs to  
```
C:\Program Files\TranscribblerApp
```  
The installer places `ffmpeg.exe` in a subfolder beneath the install directory, appends that folder to the system PATH, creates Start‑menu and desktop shortcuts, and then runs a final `--help` check to verify functionality.

Hugging Face Access Token  
Speaker diarisation relies on the `pyannote/speaker‑diarization` model, which requires licence acceptance on Hugging Face and a valid access token. Sign in at https://huggingface.co, go to Settings → Access Tokens, generate a new token with read scope, and copy the `hf_…` string.

In PowerShell you can set this token for the current session by running  
```powershell
$env:PYANNOTE_AUTH_TOKEN = "hf_your_generated_token"
```  
or make it permanent across sessions by running  
```powershell
setx PYANNOTE_AUTH_TOKEN "hf_your_generated_token"
```  
then closing and reopening PowerShell. As an alternative you may supply the token directly on the command line with the `--pyannote-token` flag.

Usage  
Open PowerShell and invoke the application with your input WAV file, desired output CSV path, Whisper model name, compute device, and token. For example:  
```powershell
& "C:\Program Files\TranscribblerApp\TranscribblerApp.exe" `
  --input "C:\path\to\input.wav" `
  --output "C:\path\to\output.csv" `
  --whisper-model base.en `
  --device cpu `
  --pyannote-token $env:PYANNOTE_AUTH_TOKEN
```  
This command transcribes the audio, assigns speaker labels to each segment, and writes a timestamped CSV with columns for start time, end time, speaker label and transcript text. On first run the diarisation model downloads to your user cache; subsequent runs reuse the local cache without requiring network access.

Troubleshooting  
If you see a “401 Unauthorized” error during diarisation, confirm that you have accepted the model licence on Hugging Face and that your `PYANNOTE_AUTH_TOKEN` environment variable is set correctly. If FFmpeg cannot be found, run  
```powershell
ffmpeg -version
```  
in PowerShell to verify that the installer appended the FFmpeg subfolder to your PATH. If it fails, you may need to adjust your PATH manually or install FFmpeg separately.

Support  
For bug reports, feature requests or documentation updates, open an issue on the TranscribblerApp GitHub repository. Contributions are welcome under the terms of the project licence.