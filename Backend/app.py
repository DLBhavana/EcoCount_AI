from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)

# ✅ Load your trained model
print("✅ Loading YOLOv11 model…")
model = YOLO("best.pt")

@app.route("/")
def home():
    return "🌳 EcoCount AI Backend is Running Successfully!"

@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img = Image.open(io.BytesIO(file.read()))

    results = model.predict(img, conf=0.25, verbose=False)[0]
    boxes = results.boxes.xyxy.tolist()

    return jsonify({
        "tree_count": len(boxes),
        "boxes": boxes
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
