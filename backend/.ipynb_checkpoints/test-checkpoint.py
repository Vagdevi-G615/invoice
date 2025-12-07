import joblib

model = joblib.load("models/checkpoint_model.pkl")
vectorizer = joblib.load("models/checkpoint_vectorizer.pkl")

sample_text = ["Invoice 12345: Payment due for vendor XYZ. GST included."]
vec = vectorizer.transform(sample_text)
pred = model.predict(vec)[0]
print(pred)
