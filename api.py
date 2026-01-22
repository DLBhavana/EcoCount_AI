# api.py
from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io
import base64
import torch

app = Flask(__name__)

# Load YOLO model
model = YOLO("best.pt")

@app.route("/detect", methods=["POST"])
def detect():
    try:
        file = request.files["file"]
        img = Image.open(file.stream)
        results = model.predict(img, conf=0.25, verbose=False)[0]
        boxes = results.boxes.xyxy.tolist()
        count = len(boxes)
        return jsonify({"tree_count": count, "boxes": boxes})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/", methods=["GET"])
def home():
    return "EcoCount AI API is running 🌳"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
