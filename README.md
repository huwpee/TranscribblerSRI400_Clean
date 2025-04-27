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

### Step 2: Create a Hugging Face Account

1. Visit [Hugging Face Sign Up Page](https://huggingface.co/join)
2. Enter your email address
3. Create a username and password
4. Click "Sign Up"
5. Complete your profile:
   - Enter your name
   - For "Company/University", enter your organization (e.g., "UNE" or "une.edu.au")
   - For "Website", enter your organization's website (e.g., "une.edu.au")
6. Verify your email address by clicking the link in the verification email

### Step 3: Accept Model Terms on Hugging Face

You MUST accept the terms for BOTH of these models:

1. Visit [pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)
   - Click the blue "Access repository" button
   - Log in if prompted
   - You'll see a screen explaining the model's license
   - Check the blue box that says "I agree to use this model under the attached license"
   - Click the blue "Access repository" button

2. Visit [pyannote/segmentation](https://huggingface.co/pyannote/segmentation)
   - Click the blue "Access repository" button
   - Log in if prompted
   - You'll see a screen explaining the model's license
   - Check the blue box that says "I agree to use this model under the attached license"
   - Click the blue "Access repository" button

### Step 4: Get Your Hugging Face Token

1. Visit [Hugging Face Tokens Page](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Name it "TranscribblerApp"
4. Select "Read" role
5. Click "Generate a token"
6. Copy the token (looks like "hf_xxxxxxxxxxxxxxxxxxxxxxxxx")

### Step 5: Install FFmpeg

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

## QUICK FIX OPTION

If you're still having trouble, try this simplified approach:

1. Run PowerShell as Administrator
2. Copy and paste this entire block:

```powershell
# Create folder for FFmpeg if it doesn't exist
if (-not (Test-Path "C:\Program Files (x86)\TranscribblerApp\bin")) {
    New-Item -Path "C:\Program Files (x86)\TranscribblerApp\bin" -ItemType Directory
}

# Download FFmpeg directly
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$ffmpegZip = "C:\Program Files (x86)\TranscribblerApp\ffmpeg.zip"
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $ffmpegZip

# Extract FFmpeg
Expand-Archive -Path $ffmpegZip -DestinationPath "C:\Program Files (x86)\TranscribblerApp\ffmpeg-temp" -Force
$ffmpegBinPath = Get-ChildItem -Path "C:\Program Files (x86)\TranscribblerApp\ffmpeg-temp" -Filter "bin" -Recurse | Select-Object -First 1 -ExpandProperty FullName
Copy-Item -Path "$ffmpegBinPath\*" -Destination "C:\Program Files (x86)\TranscribblerApp\bin" -Force

# Clean up
Remove-Item -Path $ffmpegZip -Force
Remove-Item -Path "C:\Program Files (x86)\TranscribblerApp\ffmpeg-temp" -Recurse -Force

# Set environment variables
$env:HF_HUB_DISABLE_SYMLINKS = "1"
$env:PYANNOTE_AUTH_TOKEN = "YOUR_TOKEN_HERE"
$env:PATH = "$env:PATH;C:\Program Files (x86)\TranscribblerApp\bin"

Write-Host "FFmpeg installed successfully. Now enter your Hugging Face token and run TranscribblerApp." -ForegroundColor Green
```

3. Replace "YOUR_TOKEN_HERE" with your actual Hugging Face token
4. Run TranscribblerApp with your desired input/output paths
"@ | Out-File -FilePath README.md -Encoding utf8

Write-Host "Created a comprehensive README.md with accurate Hugging Face account setup instructions" -ForegroundColor Green
```
