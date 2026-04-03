"""
Download NVIDIA Audio2Face-3D dataset sample
"""
import requests
import os
from pathlib import Path

def main():
    base_dir = Path("data/raw/nvidia")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample from NVIDIA
    urls = [
        "https://huggingface.co/nvidia/Audio2Face-3D-Dataset-v1.0.0-claire/resolve/main/audio/sample.wav",
        "https://huggingface.co/nvidia/Audio2Face-3D-Dataset-v1.0.0-claire/resolve/main/blendshapes/sample.npy"
    ]
    
    for url in urls:
        filename = url.split('/')[-1]
        r = requests.get(url)
        with open(base_dir / filename, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded {filename}")
    
    print("NVIDIA Audio2Face sample downloaded. Full dataset requires license agreement.")

if __name__ == "__main__":
    main()