from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import hashlib

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:5173"}}) 

UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def calculate_sha256(filepath, blocksize=65536):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            buffer = file.read(blocksize)
            while len(buffer) > 0:
                sha256_hash.update(buffer)
                buffer = file.read(blocksize)
        return sha256_hash.hexdigest()
    except Exception:
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({"error": f"Failed to save file: {e}"}), 500

        file_sha256 = calculate_sha256(file_path)

        if file_sha256:
            return jsonify({
                "message": f"File '{filename}' uploaded successfully!",
                "path": file_path,
                "sha256_hash": file_sha256
            }), 200
        else:
            return jsonify({"error": "File uploaded, but failed to calculate SHA256 hash."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)