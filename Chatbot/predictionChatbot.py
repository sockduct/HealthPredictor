import joblib
import numpy as np
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

# Load Random Forest model
model = joblib.load("ckd_model.pkl")

def make_prediction(input_data):
    """Make CKD prediction and return prediction and probability."""
    prediction = model.predict([input_data])
    probability = model.predict_proba([input_data])
    return prediction[0], probability

def analyze_prediction(features, prediction):
    """Explain why the model made a certain prediction based on feature importance."""
    feature_importance = model.feature_importances_
    important_factors = sorted(zip(features, feature_importance), key=lambda x: x[1], reverse=True)[:3]

    explanation = f"The model predicted {'CKD present' if prediction == 1 else 'No CKD'} because:\n"
    for feature, importance in important_factors:
        explanation += f"- {feature} had a high impact ({importance:.2f})\n"
    
    # Suggest prevention tips or advice based on the prediction
    if prediction == 1:
        prevention_tips = "To reduce CKD risk, consider controlling diabetes, reducing salt intake, and staying hydrated."
    else:
        prevention_tips = "Keep maintaining a healthy lifestyle with proper hydration and regular check-ups."

    return explanation + "\n" + prevention_tips

# Set up the OpenAI Chatbot environment
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    if load_dotenv('.env') is False:
        raise TypeError
except TypeError:
    print('Unable to load .env file.')
    quit()

llm = AzureChatOpenAI(
    deployment_name=os.environ['MODEL'],
    openai_api_version=os.environ['API_VERSION'],
    openai_api_key=os.environ['OPENAI_API_KEY'],
    azure_endpoint=os.environ['OPENAI_API_BASE'],
    openai_organization=os.environ['OPENAI_ORGANIZATION']
)

# Read context from a .txt file
try:
    with open('context.txt', 'r') as file:
        context = file.read().strip()
except FileNotFoundError:
    print("The context.txt file was not found.")
    quit()

# Initial system message for the chatbot
messages = [
    ("system", f"You are a helpful assistant. The following context may help in answering questions:\n{context}"),
]

print("You can start chatting with the assistant. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    
    # Exit if the user types 'exit' or 'quit'
    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
    
    # If the user wants to make a prediction (could be triggered by a keyword or user intent)
    if "predict" in user_input.lower():
        print("Please enter the following health values:")

        try:
            # Gather user inputs for prediction
            specific_gravity = float(input("Specific Gravity: "))
            hemoglobin = float(input("Hemoglobin: "))
            serum_creatinine = float(input("Serum Creatinine: "))
            albumin = float(input("Albumin: "))
            packed_cell_volume = float(input("Packed Cell Volume: "))
            diabetes_mellitus = int(input("Diabetes Mellitus (0 or 1): "))
            hypertension = int(input("Hypertension (0 or 1): "))
            blood_glucose_random = float(input("Blood Glucose Random: "))
            red_blood_cell_count = float(input("Red Blood Cell Count: "))
            blood_urea = float(input("Blood Urea: "))

            user_features = [specific_gravity, hemoglobin, serum_creatinine, albumin, 
                             packed_cell_volume, diabetes_mellitus, hypertension, 
                             blood_glucose_random, red_blood_cell_count, blood_urea]

            # Get the prediction and explanation
            prediction, probability = make_prediction(user_features)
            explanation = analyze_prediction(
                ['specific_gravity', 'hemoglobin', 'serum_creatinine', 'albumin', 
                 'packed_cell_volume', 'diabetes_mellitus', 'hypertension', 
                 'blood_glucose_random', 'red_blood_cell_count', 'blood_urea'], prediction
            )

            # Display the result to the user
            print(f"Assistant: The prediction is {'CKD present' if prediction == 1 else 'No CKD'}.")
            print(f"Assistant: {explanation}")
        
        except ValueError:
            print("Assistant: Please enter valid numerical values for prediction.")

    # Add user input to chatbot conversation history
    messages.append(("human", user_input))
    
    # Send conversation history to the model for a response
    response = llm.invoke(messages)
    
    # Output the model's response
    print(f"Assistant: {response.content}")
    
    # Optionally, add assistant's response to the conversation history
    messages.append(("assistant", response.content))
