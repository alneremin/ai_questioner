# Client question handler

*A simple command-line utility for recording and processing client questions using local LLMs*

---

## Prerequisites

- Python 3.8 or higher
- `curl` (for Ollama installation)

---

## Installation

### Install Ollama and required models

```bash
# install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# pull the required models
ollama pull llama3
ollama pull mxbai-embed-large

# Start Ollama server (keep this terminal open)
ollama serve
```

### Install dependencies

```bash
pip3 install -r requirements.txt
```

### Configuration

The parameters.yaml file controls all aspects of the application. Below is a complete example with explanations for each parameter.

```yaml
google_sheet_service:
  service_name: sheets
  service_version: v4
  spreadsheet_id: YOUR_SPREADSHEET_ID_HERE
  scopes:
    - https://www.googleapis.com/auth/spreadsheets
  sheet: YOUR_SHEET_NAME
  path_to_creds: ./path/to/credentials.json

llm:
  path_to_docs: ./docs
  docs_extension: txt
  chunk_size: 500
  chunk_overlap: 0
  path_to_vector_db: ./chroma_db
  embeddings_model: mxbai-embed-large
  llm: llama3
  system_prompt_path: ./config/prompt.txt
```

## Run

```bash
python3 -W ignore::UserWarning -W ignore::FutureWarning main.py ./config/parameters.yaml
```

## Diagnostics

### Check Ollama status

```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# List installed models
ollama list
```

### Test models

```bash
# Test LLM model
ollama run llama3 "Hello, how are you?"

# Test embedding model
ollama run mxbai-embed-large "test sentence"
```