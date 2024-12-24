# Ollama Chat Interface

A Streamlit-based web interface for interacting with Ollama language models using colab and ngrok to run the model.

## Prerequisites

- Python 3.x
- Streamlit
- Access to Ollama API endpoint (run the ipython notebook to start the API)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install streamlit requests
```
## Configuration
The application connects to an Ollama API endpoint configured via the OLLAMA_BASE_URL variable in the code. Currently set to use an ngrok tunnel:

```python
OLLAMA_BASE_URL="https://random-word-string.ngrok-free.app"
```

## Usage

Run the Streamlit app:
```bash
streamlit run ollama.py
```

