{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "eba3baaf-5756-4bb9-9502-5ab54e1f3db2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# app.py\n",
    "from fastapi import FastAPI\n",
    "from pydantic import BaseModel\n",
    "import joblib\n",
    "# Load checkpoint model + vectorizer\n",
    "model = joblib.load(\"models/checkpoint_model.pkl\")\n",
    "vectorizer = joblib.load(\"models/checkpoint_vectorizer.pkl\")\n",
    "# FastAPI app\n",
    "app = FastAPI(title=\"Invoice Classifier\")\n",
    "# Request schema\n",
    "class InvoiceText(BaseModel):\n",
    "    text: str\n",
    "# Predict endpoint\n",
    "@app.post(\"/predict\")\n",
    "def predict_invoice(data: InvoiceText):\n",
    "    text = data.text\n",
    "    # Optional: same cleaning as training\n",
    "    import re\n",
    "    from nltk.corpus import stopwords\n",
    "    from nltk.stem import WordNetLemmatizer\n",
    "    stop_words = set(stopwords.words(\"english\"))\n",
    "    lemmatizer = WordNetLemmatizer()   \n",
    "    def clean_text(text):\n",
    "        text = text.lower()\n",
    "        text = re.sub(r\"[^a-zA-Z\\s]\", \" \", text)\n",
    "        words = text.split()\n",
    "        words = [w for w in words if w not in stop_words]\n",
    "        words = [lemmatizer.lemmatize(w) for w in words]\n",
    "        return \" \".join(words)  \n",
    "    cleaned = clean_text(text)\n",
    "    vec = vectorizer.transform([cleaned])\n",
    "    pred = model.predict(vec)[0]\n",
    "    return {\"prediction\": pred}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "209973e4-4a5e-439f-ac63-ca5e3b559bff",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
