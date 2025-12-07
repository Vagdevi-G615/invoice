import joblib
import pandas as pd

MODEL_PATH = "models/improved_invoice_model.pkl"
VECTORIZER_PATH = "models/improved_tfidf_vectorizer.pkl"

# Load model & vectorizer using joblib
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Load CSV
INPUT_CSV = "data/realistic_invoices.csv"
OUTPUT_CSV = "invoice_predictions.csv"

df = pd.read_csv(INPUT_CSV)

possible_cols = ["text", "label"]
text_col = None

for col in possible_cols:
    if col in df.columns:
        text_col = col
        break

if text_col is None:
    raise ValueError(
        f"No valid text column found! Columns in CSV: {list(df.columns)}"
    )

print(f"Using column: {text_col}")

# Vectorize & predict
df["prediction"] = model.predict(vectorizer.transform(df[text_col].astype(str)))

# Save
df.to_csv(OUTPUT_CSV, index=False)
print(f"✔ Batch inference completed and saved to {OUTPUT_CSV}")
