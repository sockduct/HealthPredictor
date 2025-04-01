import joblib
import numpy as np
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

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
     
    # Add user input to chatbot conversation history
    messages.append(("human", user_input))
    
    # Send conversation history to the model for a response
    response = llm.invoke(messages)
    
    # Output the model's response
    print(f"Assistant: {response.content}")
    
    # Optionally, add assistant's response to the conversation history
    messages.append(("assistant", response.content))
