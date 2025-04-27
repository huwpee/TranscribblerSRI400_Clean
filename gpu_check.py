import torch
import platform
import sys

print("\n=== SYSTEM INFORMATION ===")
print(f"Python version: {platform.python_version()}")
print(f"PyTorch version: {torch.__version__}")
print(f"System: {platform.system()} {platform.release()}")
print(f"Processor: {platform.processor()}")

print("\n=== CUDA INFORMATION ===")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")
print(f"CUDA version: {torch.version.cuda if torch.cuda.is_available() else 'Not available'}")

if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        print(f"Device {i}: {torch.cuda.get_device_name(i)}")
else:
    print("No CUDA devices detected - using CPU processing")