```powershell
@"
# TranscribblerApp - Audio Speaker Identification & Transcription

## REQUIRED SETUP STEPS

### Step 1: Run PowerShell as Administrator

1. Click the Windows Start button
2. Type "PowerShell"
3. Right-click on "Windows PowerShell" in the search results
4. Select "Run as administrator"
5. Click "Yes" when prompted by User Account Control

### Step 2: Accept Model Terms on Hugging Face

You MUST accept the terms for BOTH of these models:

1. Visit [pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)
   - Click the blue "Access repository" button
   - Log in if prompted
   - Check "I accept the terms and conditions"
   - Click "Accept"

2. Visit [pyannote/segmentation](https://huggingface.co/pyannote/segmentation)
   - Click the blue "Access repository" button
   - Log in if prompted
   - Check "I accept the terms and conditions"
   - Click "Accept"

### Step 3: Get Your Hugging Face Token

1. Visit [Hugging Face Tokens Page](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Name it "TranscribblerApp"
4. Select "Read" role
5. Click "Generate a token"
6. Copy the token (looks like "hf_xxxxxxxxxxxxxxxxxxxxxxxxx")

### Step 4: Install FFmpeg

1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.zip)
2. Extract the ZIP file to C:\\ffmpeg
3. Copy these files from C:\\ffmpeg\\bin:
   - ffmpeg.exe
   - ffprobe.exe
4. Paste them into C:\\Program Files (x86)\\TranscribblerApp

## RUNNING THE APPLICATION

Copy and paste these commands into your Administrator PowerShell window:

```powershell
# Disable symlinks to avoid permission issues
$env:HF_HUB_DISABLE_SYMLINKS = "1"

# Set your Hugging Face token (replace with your actual token)
$env:PYANNOTE_AUTH_TOKEN = "YOUR_TOKEN_HERE"

# Run TranscribblerApp
& "C:\Program Files (x86)\TranscribblerApp\TranscribblerApp.exe" `
  --input "C:\Users\YOUR_USERNAME\Desktop\input.wav" `
  --output "C:\Users\YOUR_USERNAME\Desktop\output.csv" `
  --whisper-model base.en `
  --device cpu `
  --pyannote-token $env:PYANNOTE_AUTH_TOKEN
```

Replace:
- "YOUR_TOKEN_HERE" with your Hugging Face token
- "YOUR_USERNAME" with your Windows username
- The input path with the path to your audio file
- The output path with where you want the results saved

## TROUBLESHOOTING

### "Could not download 'pyannote/speaker-diarization' pipeline"
- You haven't accepted the terms for the speaker-diarization model
- Visit https://huggingface.co/pyannote/speaker-diarization and accept the terms

### "Could not download 'pyannote/segmentation' model"
- You haven't accepted the terms for the segmentation model
- Visit https://huggingface.co/pyannote/segmentation and accept the terms

### "The system cannot find the file specified"
- FFmpeg is not installed correctly
- Make sure ffmpeg.exe and ffprobe.exe are in the TranscribblerApp folder

### "OSError: [WinError 1314] A required privilege is not held by the client"
- You're not running PowerShell as Administrator
- Close PowerShell and follow Step 1 again

### "Invalid header value"
- Your token has extra spaces or newlines
- Make sure to set it correctly: $env:PYANNOTE_AUTH_TOKEN = "YOUR_TOKEN_HERE"
"@ | Out-File -FilePath README.md -Encoding utf8

Write-Host "Created a simplified README.md with clear step-by-step instructions" -ForegroundColor Green
```
