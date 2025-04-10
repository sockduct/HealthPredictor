from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
import pandas as pd
from flask import session
# Import context and Azure LLM
from contextChatbot import llm, general_context

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scretkeyforckdsession12aiproject'
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

with open('ckd_model.pkl', 'rb') as f:
    model = pickle.load(f)
       
columns = [
    'specific_gravity', 'hemoglobin', 'serum_creatinine', 'albumin',
    'packed_cell_volume', 'diabetes_mellitus', 'hypertension',
    'blood_glucose_random', 'red_blood_cell_count', 'blood_urea'
]

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        data = request.json

        features = np.array([
            float(data['specific_gravity']),
            float(data['hemoglobin']),
            float(data['serum_creatinine']),
            float(data['albumin']),
            float(data['packed_cell_volume']),
            int(data['diabetes_mellitus']),
            int(data['hypertension']),
            float(data['blood_glucose_random']),
            float(data['red_blood_cell_count']),
            float(data['blood_urea']),
        ])

        features_df = pd.DataFrame([features], columns=columns)
        prediction = model.predict(features_df)

        prediction_result = int(prediction[0])
        # print("Predictions:", prediction_result)
        
        global patient_data
        patient_data = {
            "features": data,  # Store raw input values
            "prediction": prediction_result
        }

        session['patient_data'] = {
            "features": data,
            "prediction": prediction_result
        }
        print("Session Data:", session.get('patient_data'))
        session.modified = True

        return jsonify({'prediction': prediction_result})

    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        data = request.get_json()
        user_input = data.get('message')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        patient_data = session.get('patient_data', None)
        print("Session Data in Chat-----------:", session.get('patient_data'))

        patient_info_section = "\n".join([f"{key}: {value}" for key, value in patient_data.get("features", {}).items()])
        prediction_result = "Positive (1) - High risk of CKD" if patient_data.get("prediction") == 1 else "Negative (0) - No immediate risk"
        print(patient_info_section)
        
        final_context = f"""
            You are a highly specialized medical assistant focused on Chronic Kidney Disease (CKD) and overall kidney health.
            You can respond to greetings and general conversational messages naturally.
            Your responses must be **strictly based** on the provided context and your verified medical knowledge about CKD and kidney health. 
            
            **IMPORTANT RULES**
            - You can answer questions about CKD and general kidney health.
            - Do NOT provide information unrelated to kidneys or CKD.
            - If a question is outside your scope, respond with:  
              *"I'm only able to answer questions related to CKD and kidney health based on the given context."*
            
            ---
            
            ### General CKD Knowledge
            {general_context}

            ### Patient Medical Data
            {patient_info_section}

            ### CKD Prediction Result
            {prediction_result}

            ---
            
            ### How to Respond
            The user is asking a question about their health. Consider:  
            - Their **medical data** and how it impacts CKD risk.  
            - The **prediction result** and its implications.  
            
            - **If the prediction is positive (1)**:  
              - Explain why the user may be at risk for CKD.  
              - Offer guidance on CKD management, lifestyle changes, and next steps (e.g., seeing a specialist).  

            - **If the prediction is negative (0)**:  
              - Reassure the user while explaining why they are not at risk.  
              - Provide general kidney health advice and ways to maintain healthy kidney function.  
              
            **Your responses must be clear, professional, and patient-friendly.**  
            """

#  Do NOT use outside knowledge or assumptions.
        messages = [("system", final_context), ("human", user_input)]

        response = llm.invoke(messages)
        return jsonify({'response': response.content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    print("App is running")
    app.run(debug=True, host="localhost", port=5050)
