# Invoice Classifier

A machine learning application that classifies invoices into different categories (e.g., utilities, purchase orders, receipts) using a trained model. The app is deployed on Render, allowing users to upload invoices and receive predictions via a web interface or API.

## Features

- Invoice Classification: Automatically classifies uploaded invoice documents into predefined categories.

- Web Interface: Upload invoices and view predictions directly from a browser.

- REST API: Programmatically classify invoices using HTTP requests.

- Preprocessing: Handles various formats (PDF, JPG, PNG) and standardizes data for model input.

- Real-time Predictions: Instant results using a deployed machine learning model.

## Tech Stack

- Backend: Python, FastAPI / Flask

- Machine Learning: PyTorch / TensorFlow / Scikit-learn (depending on your model)

- Frontend: React

- Deployment: Render

## Installation (Local Development)

- Clone the repository:

git clone https://github.com/Vagdevi-G615/invoice.git

cd invoice

- Create a virtual environment:

python -m venv venv

source venv/bin/activate   # Linux/Mac

venv\Scripts\activate      # Windows

- Install dependencies:

pip install -r backend/requirements.txt


- Run the application locally:

`uvicorn main:app --reload` if FastAPI

- Access the app:
Open your browser at http://127.0.0.1:8000

## Deployment on Render
 
### Steps to deploy on Render:

- Sign up / log in to Render

- Click New → Web Service.

- Connect your GitHub repository.

- Configure the service:

Environment: Python

Build Command: pip install -r backend/requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Click Create Web Service.

- Render automatically deploys your app.

## Usage
- Web Interface

- Open the app in your browser.

- Upload an invoice (PDF, JPG, PNG).

- View the predicted category.

## API

### Endpoint:

- POST /predict

- Request Example:

- curl -X POST "https://your-app-name.onrender.com/predict" \
  -F "file=@invoice.pdf"


- Response Example:

{
  "filename": "invoice.pdf",
  "predicted_category": "Utilities"
}


## Future Enhancements

- Multi-language invoice classification

- Extract key fields (amount, date, vendor) using OCR

- Dashboard to visualize invoice trends

## License
This project is licensed under the MIT License.
