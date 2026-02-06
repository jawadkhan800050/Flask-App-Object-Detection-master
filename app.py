# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

from app_helper import get_detected_image

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = os.path.join("static", "uploads")
DETECT_FOLDER = os.path.join("static", "detections")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/uploader", methods=["POST"])
def upload_file():

    # 1️⃣ Check file exists
    if "file" not in request.files:
        return "No file part", 400

    f = request.files["file"]

    # 2️⃣ Check filename
    if f.filename == "":
        return "No selected file", 400

    # 3️⃣ Secure filename
    filename = secure_filename(f.filename)
    upload_path = os.path.join(UPLOAD_FOLDER, filename)

    # 4️⃣ Save uploaded file
    f.save(upload_path)

    # 5️⃣ Run object detection
    detected_objects = get_detected_image(upload_path, filename)

    # 🔒 VERY IMPORTANT: make data Jinja-safe
    if detected_objects is None:
        detected_objects = []

    elif isinstance(detected_objects, str):
        detected_objects = [obj.strip() for obj in detected_objects.split(",") if obj.strip()]

    else:
        detected_objects = list(detected_objects)

    # 6️⃣ Render result page
    return render_template(
        "uploaded.html",
        display_detection=filename,
        detected_objects=detected_objects
    )


if __name__ == "__main__":
    app.run(debug=True)
