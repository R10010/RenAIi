"""
Download Meta Seamless Interaction dataset (subset for testing)
Full dataset requires access request, but we'll use a public sample.
"""
import requests
import os
from pathlib import Path

def download_file(url, dest):
    r = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {dest}")

def main():
    base_dir = Path("data/raw/meta")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Public sample from Meta's research page (small demo)
    sample_url = "https://dl.fbaipublicfiles.com/seamless/datasets/sample_metadata.json"
    download_file(sample_url, base_dir / "sample_metadata.json")
    
    print("Meta Seamless sample downloaded. For full dataset, visit https://ai.meta.com/resources/models-and-libraries/seamless-communication/")

if __name__ == "__main__":
    main()