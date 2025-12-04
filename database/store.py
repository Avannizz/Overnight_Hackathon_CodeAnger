import json
import os

DB_PATH = "fingerprints/original.json"

os.makedirs("fingerprints", exist_ok=True)

def save_original(sha, phash, audio):
    data = {
        "sha": sha,
        "phash": phash,
        "audio": audio
    }
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_original():
    if not os.path.exists(DB_PATH):
        return None
    with open(DB_PATH, "r") as f:
        return json.load(f)
