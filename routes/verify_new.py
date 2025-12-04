from flask import Blueprint, request, jsonify
import os
from utils.hasher import get_sha256
from utils.phash import get_video_phash
from utils.audio_fingerprint import get_audio_fingerprint
from utils.verifier import phash_similarity, audio_similarity
from database.store import load_original

verify_new = Blueprint("verify_new", __name__)

@verify_new.route("/verify-new", methods=["POST"])
def verify_new_video():
    original = load_original()

    if original is None:
        return jsonify({"error": "No original video stored"}), 400

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No video uploaded"}), 400

    path = os.path.join("uploads", "new.mp4")
    file.save(path)

    sha_new = get_sha256(path)
    phash_new = get_video_phash(path)
    audio_new = get_audio_fingerprint(path)

    result = {
        "sha256_match": sha_new == original["sha"],
        "phash_similarity": phash_similarity(original["phash"], phash_new),
        "audio_similarity": audio_similarity(original["audio"], audio_new)
    }

    return jsonify(result)
