import streamlit as st
import requests

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
    endpoint = "https://losqfanm1rbvckyl.eu-west-1.aws.endpoints.huggingface.cloud"
    response = requests.post(endpoint, json=data)
    response_data = response.json()
    
    return response_data[0]["generated_text"]

# Initialize session state for storing conversation
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Sidebar for settings
st.sidebar.header("Settings")
top_k = st.sidebar.number_input("Top K", min_value=0, max_value=100, value=30)
top_p = st.sidebar.number_input("Top P", min_value=0.0, max_value=1.0, value=0.9)
temperature = st.sidebar.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=0, max_value=512, value=512)

# Main chat interface
st.title("Marcaps Chatbot")

# Function to display messages
def display_message(index, speaker, message):
    if speaker == 'user':
        st.text_area(f"You: ", value=message, height=50, key=f"msg_{index}_user", disabled=True)
    else:
        st.text_area(f"Msrcaps: ", value=message, height=100, key=f"msg_{index}_bot", disabled=True)

# Display conversation history
for index, (speaker, message) in enumerate(reversed(st.session_state['conversation'])):
    display_message(index, speaker, message)

# User input for new message
user_input = st.text_input("You: ", value='', key="new_user_input")

# Send button
send_button = st.button("Send")

# When the user submits a new message
if send_button and user_input:
    st.session_state['conversation'].append(('user', user_input))
    bot_response = get_bot_response(user_input, top_k, top_p, temperature, max_tokens)
    st.session_state['conversation'].append(('bot', bot_response))
    # Clear the input box by rerunning the app
    st.experimental_rerun()
