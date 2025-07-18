# Retail Data Analysis Chatbot

A powerful chatbot that analyzes retail sales data using Ollama/Mistral to provide insights about order demands, sales trends, and customer data.

## Features

- **Natural Language Queries**: Ask questions in plain English like "How many order demand in April 2016?"
- **Data Analysis**: Automatic analysis of order demands, sales trends, and customer data
- **Interactive Interface**: Easy-to-use chat interface with example queries
- **Visualizations**: Automatic generation of charts and graphs
- **Ollama/Mistral Integration**: Uses local LLM for understanding complex queries

## Setup Instructions

### 1. Install Ollama

First, install Ollama on your system:

**macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

### 2. Pull Mistral Model

```bash
ollama pull mistral
```

### 3. Start Ollama Service

```bash
ollama serve
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Jupyter Notebook (Recommended)

1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `retail_chatbot.ipynb`

3. Run all cells in order

4. Use the interactive interface to ask questions

### Option 2: Python Script

1. Navigate to the directory:
```bash
cd /path/to/retail_data
```

2. Run the script:
```bash
python retail_chatbot.py
```

3. Ask questions interactively

## Example Queries

- **"How many order demand in April 2016?"**
- **"Show me the sales summary"**
- **"What are the monthly trends in 2016?"**
- **"Show me the top products"**
- **"Analyze customer data"**
- **"What's the total demand for Q1 2016?"**
- **"Compare sales between 2015 and 2016"**

## Dataset Requirements

The chatbot expects a CSV file named `Sheet1-1-Retail_Dataset2.csv` with the following characteristics:

- **Date columns**: Columns containing 'date' or 'time' in the name
- **Quantity columns**: Columns containing 'quantity', 'demand', or 'qty' in the name
- **Product columns**: Columns containing 'product' or 'item' in the name
- **Customer columns**: Columns containing 'customer' or 'client' in the name

## Troubleshooting

### Ollama Not Running
```
Error: Ollama is not running. Please start Ollama and ensure the mistral model is available.
```

**Solution:**
1. Start Ollama: `ollama serve`
2. Verify model is available: `ollama list`

### Dataset Not Found
```
Error loading dataset: [Errno 2] No such file or directory: 'Sheet1-1-Retail_Dataset2.csv'
```

**Solution:**
1. Ensure the CSV file is in the same directory as the script
2. Check the filename spelling

### Missing Dependencies
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
pip install -r requirements.txt
```

## File Structure

```
retail_data/
├── retail_chatbot.ipynb      # Jupyter notebook version
├── retail_chatbot.py         # Python script version
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── Sheet1-1-Retail_Dataset2.csv  # Your retail dataset
└── chat.ipynb               # Original empty notebook
```

## Customization

### Adding New Query Types

To add support for new query types, modify the `process_query` method in the `QueryProcessor` class:

```python
def process_query(self, query):
    query_lower = query.lower()
    
    # Add your new query type here
    if 'your_new_query_type' in query_lower:
        # Your custom logic here
        return "Your custom response"
    
    # ... existing code ...
```

### Changing the Model

To use a different Ollama model, modify the model name in the `OllamaChatbot` class:

```python
chatbot = OllamaChatbot(model_name="llama2")  # or any other model
```

## Performance Tips

1. **Large Datasets**: For datasets with >1M rows, consider sampling for faster responses
2. **Memory Usage**: Close other applications when running large analyses
3. **Ollama Performance**: Ensure sufficient RAM for the Mistral model (4GB+ recommended)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify Ollama is running: `curl http://localhost:11434/api/tags`
3. Check dataset format and column names
4. Ensure all dependencies are installed correctly 