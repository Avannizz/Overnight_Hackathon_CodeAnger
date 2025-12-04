import hashlib
from flask import Flask, request, jsonify
from PIL import Image
import imagehash
import os

app = Flask(__name__)

# Fake blockchain (for demo)
blockchain = []

PHASH_THRESHOLD = 10

def compute_sha256(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def compute_phash(file_path):
    image = Image.open(file_path)
    return imagehash.phash(image)

def is_similar(ph1, ph2):
    return abs(ph1 - ph2) <= PHASH_THRESHOLD

@app.route('/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    user = request.form.get('user', 'unknown_user')

    # Save temporarily
    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    sha256 = compute_sha256(temp_path)
    phash = compute_phash(temp_path)

    # scan blockchain
    for entry in blockchain:
        if sha256 == entry["sha256"]:
            os.remove(temp_path)
            return jsonify({
                "status": "rejected",
                "reason": "Exact duplicate detected",
                "original_owner": entry["owner"]
            }), 200

        if is_similar(phash, entry["phash"]):
            os.remove(temp_path)
            return jsonify({
                "status": "rejected",
                "reason": "Similar/edited copy detected",
                "original_owner": entry["owner"]
            }), 200

    # If new → register
    blockchain.append({
        "sha256": sha256,
        "phash": phash,
        "owner": user
    })

    os.remove(temp_path)

    return jsonify({
        "status": "registered",
        "owner": user
    }), 200


@app.route('/blockchain', methods=['GET'])
def show_blockchain():
    return jsonify([
        {
            "sha256": entry["sha256"],
            "phash": str(entry["phash"]),
            "owner": entry["owner"]
        }
        for entry in blockchain
    ]), 200

if __name__ == "__main__":
    app.run(debug=True)

