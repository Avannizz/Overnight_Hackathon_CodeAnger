import hashlib
from flask_cors import CORS


from flask import Flask, request, jsonify
from PIL import Image
import imagehash
import os

# ------------------ AI FINGERPRINT IMPORTS ------------------
import clip
import torch
import numpy as np
# ------------------------------------------------------------

app = Flask(__name__)
CORS(app)
# Fake blockchain (for demo)
blockchain = []

PHASH_THRESHOLD = 10
AI_THRESHOLD = 0.85  # similarity threshold

# ------------------ SHA256 FUNCTION ------------------
def compute_sha256(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# ------------------ pHASH FUNCTION ------------------
def compute_phash(file_path):
    image = Image.open(file_path)
    return imagehash.phash(image)

def is_similar(ph1, ph2):
    return abs(ph1 - ph2) <= PHASH_THRESHOLD

# ------------------ AI FINGERPRINT SETUP ------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def compute_ai_fingerprint(file_path):
    image = preprocess(Image.open(file_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image)

    embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding.cpu().numpy().tolist()[0]  # 512D list

def ai_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

# ------------------------------------------------------------


@app.route('/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    user = request.form.get('user', 'unknown_user')

    # Save temporarily
    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    # Compute hashes
    sha256 = compute_sha256(temp_path)
    phash = compute_phash(temp_path)
    ai_fp = compute_ai_fingerprint(temp_path)

    # ------------------ CHECK AGAINST BLOCKCHAIN ------------------
    for entry in blockchain:

        # 1️⃣ Exact duplicate — SHA-256
        if sha256 == entry["sha256"]:
            os.remove(temp_path)
            return jsonify({
                "status": "rejected",
                "reason": "Exact duplicate detected",
                "original_owner": entry["owner"]
            }), 200

        # 2️⃣ Slightly modified — pHash
        if is_similar(phash, entry["phash"]):
            os.remove(temp_path)
            return jsonify({
                "status": "rejected",
                "reason": "Similar image detected (pHash match)",
                "original_owner": entry["owner"]
            }), 200

        # 3️⃣ Heavily modified — AI Fingerprint
        if "ai_fp" in entry:
            sim = ai_similarity(ai_fp, entry["ai_fp"])
            if sim > AI_THRESHOLD:
                os.remove(temp_path)
                return jsonify({
                    "status": "rejected",
                    "reason": "AI fingerprint match (heavily transformed copy)",
                    "similarity": sim,
                    "original_owner": entry["owner"]
                }), 200

    # ------------------ IF NEW → REGISTER ------------------
    blockchain.append({
        "sha256": sha256,
        "phash": phash,
        "ai_fp": ai_fp,
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
