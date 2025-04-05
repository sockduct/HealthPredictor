### Kidney Disease Prediction API

This is a Flask-based REST API that uses a trained Random Forest model to predict the likelihood of chronic kidney disease based on medical input data.

### Features

Accepts JSON data through a POST request.
Predicts using a trained Random Forest model (ckd_model.pkl).
Returns the prediction in JSON format.
CORS enabled for cross-origin requests.

### Requirements
Install the required Python packages using:
pip install -r requirements.txt

### How to Run
Make sure you have the trained model file ckd_model.pkl in the same directory.

Run the Flask app:
python app.py

The app will start on http://127.0.0.1:5000.

### API Endpoint
POST /predict