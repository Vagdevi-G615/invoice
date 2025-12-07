from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load model + vectorizer
model = joblib.load("models/checkpoint_model.pkl")
vectorizer = joblib.load("models/checkpoint_vectorizer.pkl")

# FastAPI app
app = FastAPI(title="Invoice Classifier")

# 🚀 Add CORS (REQUIRED for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # allow all origins (React frontend)
    allow_credentials=True,
    allow_methods=["*"],         # IMPORTANT: allows OPTIONS request
    allow_headers=["*"],
)

# Request schema
class InvoiceText(BaseModel):
    text: str

# Cleaning function
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

# Prediction endpoint
@app.post("/predict")
def predict_invoice(data: InvoiceText):
    try:
        cleaned = clean_text(data.text)
        vec = vectorizer.transform([cleaned])
        pred = model.predict(vec)[0]
        return {"prediction": pred}

    except Exception as e:
        return {"error": str(e)}
from fastapi import UploadFile, File
from PIL import Image
import pytesseract
import io
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Read file
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes))

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(img)

        cleaned = clean_text(extracted_text)
        vec = vectorizer.transform([cleaned])
        pred = model.predict(vec)[0]

        return {
            "extracted_text": extracted_text,
            "prediction": pred
        }

    except Exception as e:
        return {"error": str(e)}
