import hashlib
from PIL import Image
import imagehash

# Simulated blockchain (list of dicts)
blockchain = []

# Threshold for pHash similarity
PHASH_THRESHOLD = 10

def compute_sha256(file_path):
    with open(file_path, "rb") as f:
        bytes_data = f.read()
        return hashlib.sha256(bytes_data).hexdigest()

def compute_phash(file_path):
    image = Image.open(file_path)
    return imagehash.phash(image)

def is_similar(phash1, phash2, threshold=PHASH_THRESHOLD):
    return abs(phash1 - phash2) <= threshold

def register_media(file_path, user_id):
    sha256 = compute_sha256(file_path)
    phash = compute_phash(file_path)

    # Check blockchain
    for entry in blockchain:
        if sha256 == entry["sha256"]:
            print("❌ Duplicate detected! Exact copy exists.")
            return False
        if is_similar(phash, entry["phash"]):
            print(f"❌ Similar media found! Already owned by: {entry['owner']}")
            return False

    blockchain.append({
        "sha256": sha256,
        "phash": phash,
        "owner": user_id
    })

    print(f"✅ Media registered successfully for user '{user_id}'")
    return True


# DEMO
print("Registering original...")
register_media("a.jpg", "user_original")

print("\nTrying to register modified...")
register_media("a_modified.jpg", "forger")
