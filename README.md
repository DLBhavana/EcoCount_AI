# 🌱 EcoCount AI  
## Automated Tree Enumeration System Using YOLOv11

EcoCount AI is an AI-driven system designed to automatically estimate **tree count, canopy density, biomass, and carbon stock** from satellite or aerial forest imagery. The project leverages **deep learning (YOLOv11)** and **remote sensing techniques** to provide a fast, scalable, and cost-effective alternative to traditional forest survey methods.

This system aims to support **forest monitoring, environmental assessment, and sustainable forest management**.

---

## 📌 Key Features

- Automated **tree detection and counting**
- **Canopy density** estimation
- **NDVI-based vegetation health analysis**
- **Biomass and carbon stock** estimation using standard forestry formulas
- Visual outputs with detected tree crowns
- Downloadable **CSV and PDF reports**
- Simple and user-friendly **web-based interface**

---

## 🧠 Methodology Overview

EcoCount AI follows a structured object detection and analysis pipeline:

1. Satellite / aerial image acquisition  
2. Image preprocessing and normalization  
3. Tree detection using **YOLOv11**  
4. Post-processing and tree counting  
5. Canopy density calculation  
6. NDVI computation  
7. Biomass estimation  
8. Carbon stock estimation  
9. Result visualization and report generation  

---

## 📐 Key Formulas Used

- **NDVI**  
  \[
  NDVI = \frac{(NIR - Red)}{(NIR + Red)}
  \]

- **Canopy Density**  
  \[
  Canopy\ Density = \frac{Total\ Canopy\ Area}{Total\ Land\ Area}
  \]

- **Carbon Stock**  
  \[
  Carbon\ Stock = 0.47 \times Biomass
  \]

---

## 🛠️ Technologies Used

- Python  
- YOLOv11  
- PyTorch  
- OpenCV  
- NumPy, Pandas  
- Gradio / Streamlit (Web UI)  
- Remote Sensing (NDVI analysis)

---

## 📂 Project Structure

