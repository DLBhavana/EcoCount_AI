import os, io, uuid, csv
import torch
from datetime import datetime
from PIL import Image, ImageDraw
import gradio as gr
from ultralytics import YOLO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ============================================
# ✅ LOAD YOLO MODEL SAFELY FOR HUGGINGFACE
# ============================================

# Load base architecture
model = YOLO("yolov8n.pt")

# Load safe weights
state_dict = torch.load("best_safe.pt", map_location="cpu")
model.model.load_state_dict(state_dict)

MODEL = model
print("✅ SAFE MODEL LOADED SUCCESSFULLY")


# ============================================
# ✅ DETECTION FUNCTION
# ============================================
def detect(image):
    results = MODEL.predict(image, imgsz=640, conf=0.25, verbose=False)[0]
    
    boxes = results.boxes.xyxy.tolist()
    ann = image.copy()
    draw = ImageDraw.Draw(ann)
    
    for x1, y1, x2, y2 in boxes:
        draw.rectangle([(x1, y1), (x2, y2)], outline="green", width=3)
    
    return ann, len(boxes)


# ============================================
# ✅ PDF BUILDER
# ============================================
def make_pdf(img, image_name, count):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    W, H = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, H - 60, "EcoCount AI – Report")

    c.setFont("Helvetica", 12)
    c.drawString(60, H - 90, f"Date: {datetime.now()}")
    c.drawString(60, H - 110, f"Image: {image_name}")
    c.drawString(60, H - 130, f"Detected Trees: {count}")

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    c.drawImage(ImageReader(img_bytes), 60, H - 480, width=480, height=360)

    c.showPage()
    c.save()
    buf.seek(0)

    return buf.read()


# ============================================
# ✅ MAIN PROCESS
# ============================================
def process(image):
    ann, count = detect(image)
    pdf_data = make_pdf(ann, "uploaded_image.jpg", count)

    pdf_name = f"EcoCount_{uuid.uuid4().hex[:5]}.pdf"
    with open(pdf_name, "wb") as f:
        f.write(pdf_data)

    return ann, count, pdf_name


# ============================================
# ✅ GRADIO APP
# ============================================
with gr.Blocks() as demo:
    gr.Markdown("# 🌳 EcoCount AI – HuggingFace Version")
    img = gr.Image(type="pil", label="Upload Image")
    btn = gr.Button("Run Detection ✅")
    out_img = gr.Image(type="pil")
    out_count = gr.Number(label="Tree Count")
    out_pdf = gr.File(label="Download PDF")

    btn.click(process, inputs=[img], outputs=[out_img, out_count, out_pdf])

demo.launch()
