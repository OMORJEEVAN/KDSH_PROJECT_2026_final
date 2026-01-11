from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import time
import run_inference

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "")

    image = request.files.get("story")
    image_url = None
    bs = request.files.get("backstory")
    bs_url = None

    if image:
        filename = secure_filename(image.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], "story.txt")
        image.save(path)

    if bs:
        filename2 = secure_filename(bs.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], "train.csv")
        bs.save(path)

    run_inference.run_inference()

    time.sleep(0.1)
    while not os.path.isfile("response.json"):
        time.sleep(0.1)
    return send_file(
        "response.json",
        mimetype="application/json")\

@app.route("/csv")
def csvd():
    return send_file(
        "results.csv",
        as_attachment=True
    )

if __name__ == "__main__":

    app.run(debug=True)
    print('WebAPP opened!')