# 🤖 Retail Data Chatbot

An intelligent chatbot that can answer questions about your retail sales data using natural language!

## Features

- **Natural Language Queries**: Ask questions in plain English
- **SQL Intelligence**: Automatically converts questions to SQL queries
- **Multiple Interfaces**: Choose between command-line and web interface
- **Real-time Responses**: Get instant answers about your data

## Prerequisites

1. **Ollama**: Make sure Ollama is installed and running with the `llama3` model
2. **Python Dependencies**: All required packages are in `requirements.txt`
3. **Data File**: Ensure `Sheet1-1-Retail_Dataset2.csv` is in the same directory

## Quick Start

### Option 1: Use the Launcher (Recommended)
```bash
python run_chatbot.py
```
Then choose your preferred interface:
- **1**: Command-line interface (simple, fast)
- **2**: Web interface (beautiful GUI)

### Option 2: Direct Launch

#### Command Line Interface
```bash
python retail_chatbot.py
```

#### Web Interface
```bash
streamlit run retail_chatbot_web.py
```

## Example Questions

You can ask questions like:

- **Sales Analysis**:
  - "Which product category had the highest sales in March 2016?"
  - "What was the total order demand for Category_005?"
  - "Show me the top 5 warehouses by sales volume"

- **Trends & Patterns**:
  - "What's the average order demand per product?"
  - "Which products had the highest demand in 2016?"
  - "How many orders were there in each month?"

- **Correlations**:
  - "What's the correlation between petrol price and order demand?"
  - "Do holidays affect sales volume?"

- **Specific Queries**:
  - "What's the total sales for Product_0033?"
  - "Show me all orders from Whse_S warehouse"
  - "Which months had the highest order demand?"

## Data Schema

The chatbot understands your data structure:

| Column | Type | Description |
|--------|------|-------------|
| Product_id | INTEGER | Unique product identifier |
| Product_Code | TEXT | Product code |
| Warehouse | TEXT | Warehouse location |
| Product_Category | TEXT | Product category |
| Date | TEXT | Order date |
| Order_Demand | INTEGER | Quantity demanded |
| Open | INTEGER | Store open status |
| Promo | INTEGER | Promotion status |
| StateHoliday | TEXT | Holiday status |
| SchoolHoliday | INTEGER | School holiday status |
| Petrol_price | INTEGER | Fuel price |

## Troubleshooting

### Common Issues

1. **"Ollama not found"**: Make sure Ollama is running and `llama3` model is installed
2. **"CSV file not found"**: Ensure `Sheet1-1-Retail_Dataset2.csv` is in the directory
3. **"Import errors"**: Run `pip install -r requirements.txt` to install dependencies

### Getting Help

- Check that Ollama is running: `ollama list`
- Verify the model is available: `ollama run llama3`
- Test the setup: `python -c "from langchain_ollama import OllamaLLM; print('OK')"`

## Advanced Usage

### Custom Questions
The chatbot can handle complex queries:
- "What's the percentage change in order demand between March and April 2016?"
- "Show me products with demand above the 90th percentile"
- "Which categories show seasonal patterns?"

### Tips for Better Results
- Be specific about time periods
- Mention specific categories or products when relevant
- Ask for comparisons when you want to see trends
- Use "top N" or "bottom N" for ranking queries

## Files

- `retail_chatbot.py` - Command-line interface
- `retail_chatbot_web.py` - Web interface using Streamlit
- `run_chatbot.py` - Launcher script
- `retail_chatbot_pyenv_fixed.ipynb` - Jupyter notebook version

Enjoy exploring your retail data! 🚀 