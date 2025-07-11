# KCG LLM Chatbot Project

This project is set up for developing chatbots using Mistral and Ollama on macOS.

## Setup

### Prerequisites
- Python 3.11+ installed
- Ollama app installed and running on your Mac
- Git (for version control)

### Quick Setup
1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the setup:**
   ```bash
   python test_setup.py
   ```

### Alternative: Use the setup script
```bash
./setup.sh
```

## Virtual Environment Details

- **Python Version:** 3.11.12
- **Location:** `/Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm/venv`
- **Activation:** `source venv/bin/activate`

## Key Packages Installed

### Core AI/ML
- `torch` - PyTorch for deep learning
- `transformers` - Hugging Face transformers library
- `numpy` - Numerical computing
- `pandas` - Data manipulation

### Ollama Integration
- `ollama` - Python client for Ollama

### Development Tools
- `jupyter` - Jupyter notebooks
- `requests` - HTTP library
- `httpx` - Modern HTTP client

## Usage

### 1. Start Jupyter Notebook
```bash
source venv/bin/activate
jupyter notebook
```

### 2. Pull a Model with Ollama
```bash
# Pull Mistral model
ollama pull mistral

# Or pull other models
ollama pull llama2
ollama pull codellama
```

### 3. Test Ollama Connection
```python
import ollama
models = ollama.list()
print(models)
```

### 4. Basic Chatbot Example
```python
import ollama

# Simple chat
response = ollama.chat(model='mistral', messages=[
    {
        'role': 'user',
        'content': 'Hello, how are you?'
    }
])
print(response['message']['content'])
```

## Project Structure
```
kcg-llm/
├── venv/                 # Virtual environment
├── retail_data/          # Your data files
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
├── test_setup.py        # Setup verification
├── chat.ipynb           # Your Jupyter notebook
└── README.md            # This file
```

## Troubleshooting

### Ollama Connection Issues
1. Make sure Ollama app is running
2. Check if Ollama service is accessible: `curl http://localhost:11434/api/tags`
3. Restart Ollama app if needed

### Package Installation Issues
1. Ensure you're in the virtual environment: `which python`
2. Upgrade pip: `pip install --upgrade pip`
3. Install packages individually if needed

### Jupyter Issues
1. Register the kernel: `python -m ipykernel install --user --name=kcg-llm`
2. Start Jupyter: `jupyter notebook`

## Next Steps

1. Open `chat.ipynb` in Jupyter
2. Pull your preferred model: `ollama pull mistral`
3. Start developing your chatbot!

## Model Recommendations

### For Chatbots
- `mistral` - Good balance of performance and speed
- `llama2` - Strong reasoning capabilities
- `codellama` - Good for code-related tasks

### For Development
- `mistral:7b` - Fast and efficient
- `llama2:7b` - Good for general tasks
- `codellama:7b` - Specialized for code 