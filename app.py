from flask import Flask, render_template
from routes.upload_original import upload_original
from routes.verify_new import verify_new

app = Flask(__name__)

# Register ONLY the new routes
app.register_blueprint(upload_original)
app.register_blueprint(verify_new)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload-original-page")
def upload_original_page():
    return render_template("upload_original.html")

@app.route("/verify-new-page")
def verify_new_page():
    return render_template("verify_new.html")

if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True)
