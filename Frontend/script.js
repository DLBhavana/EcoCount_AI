console.log("EcoCount AI frontend loaded ✅");

const BACKEND_URL = "https://bhavana21-backend.hf.space/predict";

const fileInput = document.getElementById("fileInput");
const runBtn = document.getElementById("runBtn");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const statusText = document.getElementById("status");

const treeCountEl = document.getElementById("treeCount");
const canopyEl = document.getElementById("canopy");
const biomassEl = document.getElementById("biomass");
const carbonEl = document.getElementById("carbon");

const btnPDF = document.getElementById("btnPDF");
const btnCSV = document.getElementById("btnCSV");

let loadedImage = null;
let pdfURL = null;
let csvURL = null;

// Image preview
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    const img = new Image();
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      loadedImage = img;
    };
    img.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});

runBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("Please upload an image first!");
    return;
  }

  statusText.textContent = "⏳ Detecting trees...";
  runBtn.disabled = true;

  const formData = new FormData();
  formData.append("image", fileInput.files[0]);

  try {
    const res = await fetch(BACKEND_URL, { method: "POST", body: formData });
    const data = await res.json();

    if (!data.ok) throw new Error("Detection failed");

    // Update metrics
    treeCountEl.textContent = data.tree_count;
    canopyEl.textContent = data.canopy_density.toFixed(3);
    biomassEl.textContent = data.biomass_tons.toFixed(2);
    carbonEl.textContent = data.carbon_tons.toFixed(2);

    // Draw annotated image
    if (data.annotated_image) {
      const img = new Image();
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
      };
      img.src = data.annotated_image;
    }

    // PDF & CSV links
    const baseURL = BACKEND_URL.replace("/predict", "");
    pdfURL = baseURL + data.pdf_download;
    csvURL = baseURL + data.csv_download;

    statusText.textContent = `✅ Detection done. Found ${data.tree_count} trees.`;
    statusText.style.color = "green";
  } catch (err) {
    console.error(err);
    statusText.textContent = "❌ Detection failed.";
    statusText.style.color = "red";
  } finally {
    runBtn.disabled = false;
  }
});

btnPDF.addEventListener("click", () => {
  if (pdfURL) window.open(pdfURL, "_blank");
  else alert("Run detection first!");
});

btnCSV.addEventListener("click", () => {
  if (csvURL) window.open(csvURL, "_blank");
  else alert("Run detection first!");
});
