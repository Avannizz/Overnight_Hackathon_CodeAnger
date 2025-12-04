from flask import Blueprint, request, jsonify
import os
from utils.verifier import verify

# define blueprint correctly — do NOT import this file anywhere inside itself
verify_route = Blueprint("verify", __name__)

@verify_route.route("/verify", methods=["POST"])
def verify_api():
    file1 = request.files.get("video1")
    file2 = request.files.get("video2")

    if not file1 or not file2:
        return jsonify({"error": "Upload 2 videos"}), 400

    # ensure uploads folder exists
    os.makedirs("uploads", exist_ok=True)

    v1 = os.path.join("uploads", file1.filename)
    v2 = os.path.join("uploads", file2.filename)

    file1.save(v1)
    file2.save(v2)

    result = verify(v1, v2)
    return jsonify(result)
