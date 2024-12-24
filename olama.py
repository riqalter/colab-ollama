import streamlit as st
import requests
import json
from typing import List

# Configure the base URL
OLLAMA_BASE_URL = "https://e792-34-145-46-106.ngrok-free.app"

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_available_models() -> List[str]:
    """Fetch available models from Ollama API"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model['name'] for model in models]
        return ["llama3.2:3b"]  # Fallback to default model
    except Exception:
        return ["llama3.2:3b"]  # Fallback to default model

def generate_response(prompt: str, model: str) -> str:
    """Generate response from Ollama API"""
    try:
        messages = [
            {
                "role": msg["role"],
                "content": msg["content"]
            } for msg in st.session_state.messages
        ]
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": True  # Changed to True for streaming
            },
            stream=True,  # Enable streaming for requests
            timeout=30
        )
        
        if response.status_code == 200:
            placeholder = st.empty()
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'message' in json_response:
                        content = json_response['message'].get('content', '')
                        full_response += content
                        placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            return full_response
            
        return f"Error: {response.status_code}"
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the server. Please check if the service is available."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

# Streamlit UI
st.title("💬 Ollama Chat Interface")

# Model selector
models = get_available_models()
selected_model = st.sidebar.selectbox("Select Model", models)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        response = generate_response(prompt, selected_model)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar options
with st.sidebar:
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()