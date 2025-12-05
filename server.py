import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import imagehash
import os
import json

import clip
import torch
import numpy as np

from web3 import Web3

app = Flask(__name__)
CORS(app)

# ---------------- GANACHE SETUP ----------------
GANACHE_URL = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
SENDER = w3.eth.accounts[0]

with open("MediaRegistry_abi.json", "r") as f:
    ABI = json.load(f)

CONTRACT_ADDRESS = "0xaF1FCb6EE3d2B5CD688eef2BC205C08c28415EE6"
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# ---------------- IMAGE HASHING ----------------
PHASH_THRESHOLD = 10
AI_THRESHOLD = 0.85

def compute_sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def compute_phash(path):
    return imagehash.phash(Image.open(path))

# ---------------- AI FINGERPRINT ----------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def compute_ai_fingerprint(path):
    img = preprocess(Image.open(path)).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = model.encode_image(img)
    emb = emb / emb.norm(dim=-1, keepdim=True)
    return emb.cpu().numpy().tolist()[0]

def ai_similarity(v1, v2):
    v1 = np.array(v1); v2 = np.array(v2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

# Store verified media locally
media_db = []

@app.route('/upload', methods=['POST'])
def upload_media():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    username = request.form.get("user", "unknown")

    temp = f"temp_{file.filename}"
    file.save(temp)

    sha256 = compute_sha256(temp)
    phash = compute_phash(temp)
    ai_fp = compute_ai_fingerprint(temp)

    # DISTILLED AI FINGERPRINT HASH FOR BLOCKCHAIN
    ai_hash = hashlib.sha256(str(ai_fp).encode()).hexdigest()

    # DUPLICATE CHECK
    for item in media_db:
        if sha256 == item["sha256"]:
            os.remove(temp)
            return jsonify({"status": "rejected", "reason": "Exact duplicate"}), 200

        if abs(phash - item["phash"]) <= PHASH_THRESHOLD:
            os.remove(temp)
            return jsonify({"status": "rejected", "reason": "pHash match"}), 200

        if ai_similarity(ai_fp, item["ai_fp"]) > AI_THRESHOLD:
            os.remove(temp)
            return jsonify({"status": "rejected", "reason": "AI fingerprint match"}), 200

    # ADD LOCALLY
    media_db.append({
        "sha256": sha256,
        "phash": phash,
        "ai_fp": ai_fp,
        "owner": username
    })

    # WRITE TO BLOCKCHAIN (compact hash = cheap gas)
    tx = contract.functions.storeMedia(
        sha256,
        str(phash),
        ai_hash
    ).transact({"from": SENDER})

    receipt = w3.eth.wait_for_transaction_receipt(tx)
    os.remove(temp)

    return jsonify({
        "status": "registered",
        "tx_hash": receipt.transactionHash.hex(),
        "owner": username
    })

@app.route('/blockchain', methods=['GET'])
def get_chain():
    return jsonify({"total_entries": contract.functions.getTotal().call()})


if __name__ == "__main__":
    app.run(debug=True)
