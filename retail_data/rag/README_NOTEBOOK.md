# Retail Chatbot Notebook Setup

This notebook demonstrates how to create a chatbot that can query retail data using SQL and Ollama.

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

2. **Virtual Environment**: The notebook is configured to use the `kcg-llm-venv` virtual environment

## Running the Notebook

### Option 1: Using the start script
```bash
cd /Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm
./start_notebook.sh
```

### Option 2: Manual startup
```bash
cd /Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm
source venv/bin/activate
cd retail_data
jupyter notebook --no-browser --port=8888
```

## Important Steps

1. **Open the notebook**: Navigate to `retail_chatbot_sql_ollama_fixed.ipynb`

2. **Select the correct kernel**: 
   - Click on "Kernel" → "Change kernel"
   - Select "KCG LLM Environment"

3. **Run the cells in order**:
   - Cell 1: Setup imports
   - Cell 2: Load data into database
   - Cell 3: Import LangChain modules
   - Cell 4: Initialize Ollama LLM
   - Cell 5: Setup database connection
   - Cell 6: Create SQL agent
   - Cell 7: Test with sample query
   - Cell 8: Interactive chat (optional)

## Troubleshooting

### If you get import errors:
- Make sure you're using the "KCG LLM Environment" kernel
- Restart the kernel if needed: Kernel → Restart

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

- `retail_chatbot_sql_ollama_fixed.ipynb`: The main notebook
- `Sheet1-1-Retail_Dataset2.csv`: Retail data
- `retail_sales.db`: SQLite database (created automatically)
- `README_NOTEBOOK.md`: This file 