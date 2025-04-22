# HealthPredictor

## CIS 579 Group 1 Healthcare Project

## Setup

* Install git - see [here](https://git-scm.com/downloads/win) for Windows
* Clone the repo from GitHub:
  `git clone https://github.com/sockduct/HealthPredictor.git`
* ~~Install Python 3.13~~
  * Note:  As of February 10, 2025 - the CatBoost Python package used in this
    Jupyter Notebook is not compatible with Python 3.13.  See [here](
    https://catboost.ai/docs/en/concepts/python-installation) for details.
* Install Python 3.12, 64 bit - see
  [here](https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe) for
  Windows as of February 10, 2025
* Setup and activate a Python virtual environment:
  * Windows:

    ```PowerShell
    PS> py -3.12 -m venv .venv
    PS> .venv\scripts\activate
    ```

* Install required libraries from within Python virtual environment from the root
  directory of the repository (where the master requirements.txt package specifications is):
  `pip install -r requirements.txt`

* Create a `.env` file with your Azure OpenAI credentials/environment in CKD_Web/Backend:

  ```env
  OPENAI_API_BASE="https://<YOUR-ENDPOINT.EXAMPLE.COM>/azure-openai-api"
  OPENAI_API_KEY="<YOUR_API_KEY>"
  OPENAI_ORGANIZATION="<YOUR-ORG-ID>"
  MODEL="gpt-4o-mini"
  API_VERSION="2024-06-01"
  ```

* Install Node.js (if not installed):

  * Follow [this guide](https://nodejs.org/en/download/) to install Node.js.

* Install Node Dependencies in the CKD_Web/UI directory (where the package.json
  dependency requirements file is):

  ```PowerShell
  PS> npm install
  ```

## Explore Notebooks

* Start the Jupyter lab environment to browse/work on the Notebooks (from the root
  directory of the repository):
  `jupyter lab`

* Dataset Exploration:
  * [Analyze Runs - 100 Random Sampling (Original Dataset)](AnalyzeRuns100Random.ipynb)
  * [Analyze Runs - 100 KNN Imputation (Original Dataset)](AnalyzeRuns100KNN.ipynb)
  * [HealthPredictor Notebook - Original Dataset](HealthPredictor.ipynb)
  * [HealthPredictor Notebook 2 - New Dataset](HealthPredictor2.ipynb)

* Note: Analyze Runs data created using `batch_collector.py`

## Try Out the Web App in Development Mode (CKD_Web)

### Kidney Disease Prediction Backend API (CKD_Web/Backend)

This is a Flask-based REST API that uses a trained Random Forest model to predict
the likelihood of chronic kidney disease based on medical input data.

#### Features

* Accepts JSON data through a POST request
* Predicts using a trained Random Forest model ('CKD-XGB.pkl')
* Returns the prediction serialized in JSON format
* CORS enabled for cross-origin requests

#### How to Run the Backend

* Make sure you have the trained model file CKD-XGB.pkl in the CKD_Web/Backend directory
* Validate .env correctly configured in the CKD_Web/Backend directory with Azure
  OpenAI LLM model details and credentials (see Setup section above)
* Run the Flask app using the development server - app runs on <http://localhost:5050>:

  ```PowerShell
  # Ensure you are running from within the activated Python virtual environment (see Setup)
  PS> python .\app.py
  ```

#### API Endpoint

POST /predict

### Kidney Disease Prediction Frontend UI (CKD_Web/UI - Next.js)

This is a frontend application built with Next.js that provides a user interface for the Kidney Disease Prediction API.

#### How to Run the Frontend

* Ensure Node.js and this app's dependencies are installed (see Setup)
* Start the development server - app runs on <http://localhost:3000>:

  ```PowerShell
  PS> npm run dev
  ```

#### Frontend App Features

* User form to input medical data
* Sends data to Flask API Backend (/predict endpoint)

### Test Web App

* Open a new tab running the webapp:
  * <a href="http://localhost:3000" target="_blank" rel="noopener noreferrer">
    Open Local Web App in New Tab</a>
  * Note:  The first time you open the web app and the first time you run each
    operation, it can take up to a minute for the app to "compile" and run...

* Patient with CKD (Patient ID - 249 from data/chronickidneydisease-uci-400x25.csv)
  * specific_gravity: 1.01
  * albumin: 4
  * hemoglobin: 3.1
  * hypertension: 1
  * serum_creatinine: 13.3
  * sodium: 124
  * white_blood_cell_count: 5400
  * blood_glucose_random: 176
  * packed_cell_volume: 9
  * age: 56

* Patient without CKD (Patient ID - 250 from data/chronickidneydisease-uci-400x25.csv)
  * specific_gravity: 1.025
  * albumin: 0
  * hemoglobin: 15
  * hypertension: 0
  * serum_creatinine: 1.2
  * sodium: 135
  * white_blood_cell_count: 10400
  * blood_glucose_random: 140
  * packed_cell_volume: 48
  * age: 40

* Example chatbot prompts for CKD patients:
  * Why do I have chronic kidney disease?
  * What is the biggest contributor?
  * What are early signs of kidney problems?
  * What foods should I limit with CKD?

* Example chatbot prompts for non-CKD patients:
  * How can I keep my kidneys healthy?
  * Where can I learn more about CKD?

* Example chatbot prompts the will be denied:
  * Where can I get the best deal on Detroit Red Wings tickets? (Non CKD question)
  * Why do I have diabetes? (Non CKD question)

### Troubleshooting

* Ensure both the Flask backend and Next.js frontend are running for the app to
  work correctly
* Ensure you start each one in the correct directory (see notes above)
* Ensure you have followed the setup directions to correctly install Python and
  Node/JavaScript dependencies
* Ensure you are running the Python backend from the correct activated virtual
  environment
* The first time you perform each operation on the web site - the first visit,
  the first patient data submission, etc. - it can take up to a minute each for
  the app to "compile."  If you view the console where you did the `npm run dev`
  to run the web app, you'll see it's progress...
