"""
Download Allo-AVA dataset sample (gesture data)
"""
import requests
from pathlib import Path

def main():
    base_dir = Path("data/raw/alloava")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample from paper's GitHub
    url = "https://github.com/facebookresearch/allo-ava/raw/main/sample_data/gesture_sequence.npy"
    r = requests.get(url)
    with open(base_dir / "gesture_sample.npy", 'wb') as f:
        f.write(r.content)
    
    print("Allo-AVA sample downloaded. Full dataset available at https://github.com/facebookresearch/allo-ava")

if __name__ == "__main__":
    main()