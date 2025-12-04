from flask import Blueprint, request, jsonify
import os
from utils.hasher import get_sha256
from utils.phash import get_video_phash
from utils.audio_fingerprint import get_audio_fingerprint
from database.store import save_original

upload_original = Blueprint("upload_original", __name__)

@upload_original.route("/upload-original", methods=["POST"])
def upload_original_video():
    if "file" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files["file"]
    path = os.path.join("uploads", "original.mp4")
    file.save(path)

    sha = get_sha256(path)
    phash = get_video_phash(path)
    audio = get_audio_fingerprint(path)

    save_original(sha, phash, audio)

    return jsonify({
        "message": "Original video stored successfully",
        "sha": sha,
        "phash": phash,
        "audio": audio
    })
