# Retail Chatbot Notebook Setup (pyenv Python 3.10.13)

This notebook demonstrates how to create a chatbot that can query retail data using SQL and Ollama using your pyenv Python 3.10.13 environment.

## Prerequisites

1. **Ollama Installation**: Make sure Ollama is installed and running
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama
   ollama serve
   
   # Pull the llama3 model
   ollama pull llama3
   ```

2. **Python Environment**: Using pyenv Python 3.10.13
   - All required packages are already installed in your pyenv environment
   - Jupyter kernel is registered as "Python 3.10.13 (pyenv)"

## Running the Notebook

### Option 1: Using the start script
```bash
cd /Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm
./start_notebook_pyenv.sh
```

### Option 2: Manual startup
```bash
cd /Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm/retail_data
/Users/ileene/.pyenv/versions/3.10.13/bin/jupyter notebook --no-browser --port=8888
```

## Important Steps

1. **Open the notebook**: Navigate to `retail_chatbot_pyenv.ipynb`

2. **Select the correct kernel**: 
   - Click on "Kernel" → "Change kernel"
   - Select "Python 3.10.13 (pyenv)"

3. **Run the cells in order**:
   - Cell 1: Setup imports and check Python environment
   - Cell 2: Load data into database
   - Cell 3: Import LangChain modules
   - Cell 4: Initialize Ollama LLM
   - Cell 5: Setup database connection
   - Cell 6: Create SQL agent
   - Cell 7: Test with sample query
   - Cell 8: Interactive chat (optional)
   - Cell 9: Sample queries

## Troubleshooting

### If you get import errors:
- Make sure you're using the "Python 3.10.13 (pyenv)" kernel
- Restart the kernel if needed: Kernel → Restart
- All required packages are already installed in your pyenv environment

### If Ollama connection fails:
- Check if Ollama is running: `ollama list`
- Make sure llama3 model is available: `ollama pull llama3`
- Test Ollama: `ollama run llama3 "Hello"`

### If database errors occur:
- Make sure the CSV file `Sheet1-1-Retail_Dataset2.csv` is in the same directory
- Check if the database file `retail_sales.db` was created successfully

## Sample Questions

Once the agent is set up, you can ask questions like:
- "Which product category had the highest sales?"
- "What was the total revenue in 2016?"
- "Show me the top 5 products by quantity sold"
- "What is the average order value?"
- "Which month had the highest sales?"

## Files

- `retail_chatbot_pyenv.ipynb`: The main notebook for pyenv environment
- `Sheet1-1-Retail_Dataset2.csv`: Retail data
- `retail_sales.db`: SQLite database (created automatically)
- `README_PYENV.md`: This file
- `start_notebook_pyenv.sh`: Start script for pyenv environment

## Environment Details

- **Python**: 3.10.13 (pyenv)
- **Location**: `/Users/ileene/.pyenv/versions/3.10.13/`
- **Kernel**: "Python 3.10.13 (pyenv)"
- **Packages**: All required packages installed via pip 