#!/usr/bin/env python3
"""
Retail Data Analysis Chatbot
A chatbot that analyzes retail sales data using Ollama/Mistral
"""

import pandas as pd
import numpy as np
import requests
import json
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RetailAnalyzer:
    def __init__(self, df):
        self.df = df
        self.date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
    def get_order_demand_by_month_year(self, month, year):
        """Get order demand for a specific month and year"""
        if not self.date_columns:
            return "No date column found in the dataset"
        
        date_col = self.date_columns[0]
        filtered_df = self.df[(self.df[date_col].dt.month == month) & 
                             (self.df[date_col].dt.year == year)]
        
        # Look for quantity or demand columns
        quantity_cols = [col for col in self.df.columns if 'quantity' in col.lower() or 'demand' in col.lower() or 'qty' in col.lower()]
        
        if quantity_cols:
            total_demand = filtered_df[quantity_cols[0]].sum()
            return f"Total order demand in {pd.Timestamp(year, month, 1).strftime('%B %Y')}: {total_demand:,.0f}"
        else:
            return f"Number of orders in {pd.Timestamp(year, month, 1).strftime('%B %Y')}: {len(filtered_df)}"
    
    def get_sales_summary(self):
        """Get overall sales summary"""
        summary = {
            'total_records': len(self.df),
            'date_range': None,
            'numeric_columns': self.numeric_columns,
            'date_columns': self.date_columns
        }
        
        if self.date_columns:
            date_col = self.date_columns[0]
            summary['date_range'] = f"{self.df[date_col].min().strftime('%Y-%m-%d')} to {self.df[date_col].max().strftime('%Y-%m-%d')}"
        
        return summary

class OllamaChatbot:
    def __init__(self, model_name="mistral"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        
    def check_ollama_status(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, user_input, context_data=None):
        """Generate response using Ollama/Mistral"""
        if not self.check_ollama_status():
            return "Error: Ollama is not running. Please start Ollama and ensure the mistral model is available."
        
        # Prepare the prompt with context
        system_prompt = """You are a helpful retail data analyst assistant. You can analyze retail sales data and provide insights. 
        When asked about data, provide clear, accurate responses based on the available information."""
        
        if context_data:
            system_prompt += f"\n\nContext data: {context_data}"
        
        prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error generating response: {str(e)}"

class QueryProcessor:
    def __init__(self, analyzer, chatbot):
        self.analyzer = analyzer
        self.chatbot = chatbot
        
    def extract_date_info(self, query):
        """Extract month and year from query"""
        # Month patterns
        month_patterns = {
            'january': 1, 'jan': 1, '1': 1,
            'february': 2, 'feb': 2, '2': 2,
            'march': 3, 'mar': 3, '3': 3,
            'april': 4, 'apr': 4, '4': 4,
            'may': 5, '5': 5,
            'june': 6, 'jun': 6, '6': 6,
            'july': 7, 'jul': 7, '7': 7,
            'august': 8, 'aug': 8, '8': 8,
            'september': 9, 'sep': 9, '9': 9,
            'october': 10, 'oct': 10, '10': 10,
            'november': 11, 'nov': 11, '11': 11,
            'december': 12, 'dec': 12, '12': 12
        }
        
        query_lower = query.lower()
        month = None
        year = None
        
        # Extract month
        for month_name, month_num in month_patterns.items():
            if month_name in query_lower:
                month = month_num
                break
        
        # Extract year (4-digit year)
        year_match = re.search(r'\b(20\d{2})\b', query)
        if year_match:
            year = int(year_match.group(1))
        
        return month, year
    
    def process_query(self, query):
        """Process user query and generate response"""
        query_lower = query.lower()
        
        # Check for specific query types
        if 'order demand' in query_lower or 'demand' in query_lower:
            month, year = self.extract_date_info(query)
            if month and year:
                result = self.analyzer.get_order_demand_by_month_year(month, year)
                return result
            else:
                return "Please specify both month and year for order demand analysis."
        
        elif 'summary' in query_lower or 'overview' in query_lower:
            summary = self.analyzer.get_sales_summary()
            return f"Dataset Summary:\n- Total records: {summary['total_records']}\n- Date range: {summary['date_range']}\n- Numeric columns: {summary['numeric_columns']}"
        
        else:
            # Use Ollama/Mistral for general questions
            context = f"Dataset has {len(self.analyzer.df)} records with columns: {list(self.analyzer.df.columns)}"
            return self.chatbot.generate_response(query, context)

def preprocess_data(df):
    """Preprocess the retail dataset"""
    df_processed = df.copy()
    
    # Convert date columns to datetime if they exist
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    for col in date_columns:
        try:
            df_processed[col] = pd.to_datetime(df_processed[col])
        except:
            pass
    
    return df_processed

def main():
    """Main function to run the chatbot"""
    print("🛍️ Retail Data Analysis Chatbot")
    print("=" * 50)
    
    # Load data
    try:
        print("Loading dataset...")
        df = pd.read_csv('Sheet1-1-Retail_Dataset2.csv')
        df_processed = preprocess_data(df)
        print(f"Dataset loaded successfully! Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    # Initialize components
    analyzer = RetailAnalyzer(df_processed)
    chatbot = OllamaChatbot()
    query_processor = QueryProcessor(analyzer, chatbot)
    
    print("\nChatbot initialized! You can ask questions about the retail data.")
    print("Example queries:")
    print("- How many order demand in April 2016?")
    print("- Show me the sales summary")
    print("- What are the trends in 2016?")
    print("- Type 'quit' to exit")
    print("=" * 50)
    
    # Interactive loop
    while True:
        try:
            query = input("\n🤖 Ask a question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not query:
                continue
            
            print(f"\n📊 Processing: {query}")
            print("-" * 30)
            
            response = query_processor.process_query(query)
            print(f"\n📈 Response:\n{response}")
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 