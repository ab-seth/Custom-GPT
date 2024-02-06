import streamlit as st
import requests
import os
from dotenv import load_dotenv



load_dotenv() # make a call before trying to access the environment variable

# Function to send requests to the Hugging Face endpoint
def get_bot_response(user_input, top_k, top_p, temperature, max_tokens):
    data = {
        "inputs": user_input,
        "parameters": {
            "top_k": top_k,
            "top_p": top_p,
            "temperature": temperature,
            "max_new_tokens": max_tokens
        }
    }
    endpoint = os.getenv('ENDPOINT_URL')
    response = requests.post(endpoint, json=data)
    response_data = response.json()
    
    # Check if the response is a list and access the first element, otherwise directly access the dictionary
    if isinstance(response_data, list):
        return response_data[0]["generated_text"]
    else:
        # If it's a dictionary, check for the 'generated_text' key
        return response_data.get("generated_text", "No response generated")

# Initialize session state for storing conversation and input counter
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'input_counter' not in st.session_state:
    st.session_state['input_counter'] = 0

# Sidebar for settings
st.sidebar.header("Settings")
top_k = st.sidebar.number_input("Top K", min_value=0, max_value=100, value=30)
top_p = st.sidebar.number_input("Top P", min_value=0.0, max_value=1.0, value=0.9)
temperature = st.sidebar.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=0, max_value=512, value=512)

# Main chat interface
st.title("Marcaps Chatbot")

# Display conversation history
for index, (speaker, message) in enumerate(st.session_state['conversation']):
    # Display past messages
    if speaker == 'user':
        st.text_area(f"You: ", value=message, height=50, key=f"msg_{index}_user", disabled=True)
    else:
        st.text_area(f"Msrcaps: ", value=message, height=100, key=f"msg_{index}_bot", disabled=True)

# Generate a unique key for the text input widget based on the input counter
input_key = f"user_input_{st.session_state['input_counter']}"

# User input for new message
user_input = st.text_input("You: ", value='', key=input_key)

# Send button
send_button = st.button("Send")

if send_button and user_input:
    st.session_state['conversation'].append(('user', user_input))
    bot_response = get_bot_response(user_input, top_k, top_p, temperature, max_tokens)
    st.session_state['conversation'].append(('bot', bot_response))
    st.session_state['input_counter'] += 1
    st.experimental_rerun()
