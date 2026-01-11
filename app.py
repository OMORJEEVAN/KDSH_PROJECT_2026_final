from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import webbrowser
import time
import run_inference
import csvtojson
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
        image_url = f"/{path}"

    if bs:
        filename2 = secure_filename(bs.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], "train.csv")
        bs.save(path)
        bs_url = f"/{path}"

    run_inference.run_inference()
    csvtojson.m2()

    while not os.path.isfile("response.json"):
        time.sleep(0.1)
    return send_file(
        "response.json",
        mimetype="application/json")

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
    print('WebAPP opened!')