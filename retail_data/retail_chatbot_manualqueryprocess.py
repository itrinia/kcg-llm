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
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, user_input, context_data=None):
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
        
        for month_name, month_num in month_patterns.items():
            if month_name in query_lower:
                month = month_num
                break
        
        year_match = re.search(r'\b(20\d{2})\b', query)
        if year_match:
            year = int(year_match.group(1))
        
        return month, year
    
    def process_query(self, query):
        query_lower = query.lower()
        
        # 1. order demand
        if 'order demand' in query_lower or 'demand' in query_lower or 'orders' in query_lower:
            month, year = self.extract_date_info(query)
            
            # Extract all 4+ digit numbers
            numbers = re.findall(r'\b\d{4,}\b', query)
            product_id = None
            if numbers:
                # Remove the year from the list if present
                numbers_wo_year = [n for n in numbers if str(year) != n]
                if numbers_wo_year:
                    product_id = numbers_wo_year[0]
                elif len(numbers) == 1 and (not year or numbers[0] != str(year)):
                    product_id = numbers[0]
            date_col = self.analyzer.date_columns[0] if self.analyzer.date_columns else None
            if month and year and date_col:
                filtered_df = self.analyzer.df[(self.analyzer.df[date_col].dt.month == month) & (self.analyzer.df[date_col].dt.year == year)]
                if product_id:
                    filtered_df = filtered_df[filtered_df[product_col].astype(str) == product_id]
                if filtered_df.empty:
                    return f"No data found for product {product_id} in {pd.Timestamp(year, month, 1).strftime('%B %Y')}."
                
                quantity_cols = [col for col in self.analyzer.df.columns if 'quantity' in col.lower() or 'demand' in col.lower() or 'qty' in col.lower()]
                if quantity_cols:
                    total_demand = filtered_df[quantity_cols[0]].sum()
                    if product_id:
                        return f"Total order demand for product {product_id} in {pd.Timestamp(year, month, 1).strftime('%B %Y')}: {total_demand:,.0f}"
                    else:
                        return f"Total order demand in {pd.Timestamp(year, month, 1).strftime('%B %Y')}: {total_demand:,.0f}"
                else:
                    if product_id:
                        return f"Number of orders for product {product_id} in {pd.Timestamp(year, month, 1).strftime('%B %Y')}: {len(filtered_df)}"
                    else:
                        return f"Number of orders in {pd.Timestamp(year, month, 1).strftime('%B %Y')}: {len(filtered_df)}"
            else:
                return "Please specify both month and year for order demand analysis."
        
        # 2. best product
        elif ('best' in query_lower or 'terbaik' in query_lower) and ('product' in query_lower or 'produk' in query_lower):
            month, year = self.extract_date_info(query)
            if not (month and year):
                return "Please specify both month and year to find the best product."
            if not all(col in self.analyzer.df.columns for col in ['Product_id', 'Order_Demand']):
                return "Dataset must have 'Product_id' and 'Order_Demand' columns for this analysis."
            date_col = self.analyzer.date_columns[0] if self.analyzer.date_columns else None
            if not date_col:
                return "No date column found in the dataset."
            filtered_df = self.analyzer.df[(self.analyzer.df[date_col].dt.month == month) & (self.analyzer.df[date_col].dt.year == year)]
            if filtered_df.empty:
                return f"No data found for {pd.Timestamp(year, month, 1).strftime('%B %Y')}."
            top_product = filtered_df.groupby('Product_id')['Order_Demand'].sum().sort_values(ascending=False).head(1)
            product_id = top_product.index[0]
            total_sales = top_product.iloc[0]
            return f"Best product in {pd.Timestamp(year, month, 1).strftime('%B %Y')} (by Product_id): {product_id} with total sales: {total_sales:,.0f}"
        
        # 3. predict top products for 2017 based on 2016 data
        elif (('produk' in query_lower or 'product' in query_lower) and ('2017' in query_lower) and ('2016' in query_lower)):
            if not all(col in self.analyzer.df.columns for col in ['Product_id', 'Order_Demand', 'Date']):
                return "Dataset must have 'Product_id', 'Order_Demand', and 'Date' columns for this analysis."
            date_col = self.analyzer.date_columns[0] if self.analyzer.date_columns else 'Date'
            df_2016 = self.analyzer.df[self.analyzer.df[date_col].dt.year == 2016]
            top_products = df_2016.groupby('Product_id')['Order_Demand'].sum().sort_values(ascending=False).head(3)
            product_ids = list(top_products.index)
            return f"Top 3 products in 2016 likely to sell well in 2017 (by Product_id): {product_ids}"
        
        # 4. total/sum queries for any numeric column
        elif ('total' in query_lower or 'sum' in query_lower):
            col_match = None
            for col in self.analyzer.numeric_columns:
                if col.lower().replace('_', ' ') in query_lower or col.lower() in query_lower:
                    col_match = col
                    break
            
            if not col_match:
                for col in self.analyzer.numeric_columns:
                    if any(word in col.lower() for word in query_lower.split()):
                        col_match = col
                        break
            if not col_match:
                return f"No matching numeric column found in the dataset for your query. Available numeric columns: {self.analyzer.numeric_columns}"
            month, year = self.extract_date_info(query)
            date_col = self.analyzer.date_columns[0] if self.analyzer.date_columns else None
            if month and year and date_col:
                filtered_df = self.analyzer.df[(self.analyzer.df[date_col].dt.month == month) & (self.analyzer.df[date_col].dt.year == year)]
            else:
                filtered_df = self.analyzer.df
            total_value = filtered_df[col_match].sum()
            if month and year:
                date_str = pd.Timestamp(year, month, 1).strftime('%B %Y')
                return f"Total {col_match} in {date_str}: {total_value:,.2f}"
            else:
                return f"Total {col_match} in the dataset: {total_value:,.2f}"
        
        # 5. Inventory & Stock
        elif 'stock' in query_lower or 'inventory' in query_lower:
            product_id = None
            for col in self.analyzer.df.columns:
                if 'product' in col.lower() and 'id' in col.lower():
                    for word in query_lower.split():
                        if word.isdigit():
                            product_id = word
                            break
            stock_col = None
            for col in self.analyzer.df.columns:
                if 'stock' in col.lower() or 'inventory' in col.lower():
                    stock_col = col
                    break
            if product_id and stock_col:
                product_rows = self.analyzer.df[self.analyzer.df['Product_id'].astype(str) == product_id]
                if not product_rows.empty:
                    current_stock = product_rows[stock_col].iloc[-1]
                    return f"Current stock for Product_id {product_id}: {current_stock}"
                else:
                    return f"No data found for Product_id {product_id}."
            elif 'stockout' in query_lower or 'out of stock' in query_lower:
                if stock_col:
                    stockout_products = self.analyzer.df[self.analyzer.df[stock_col] == 0]['Product_id'].unique()
                    return f"Products out of stock: {list(stockout_products)}"
                else:
                    return "No stock column found in the dataset."
            else:
                return "Please specify a Product_id or ask about stockouts."

        # 6. Promotions & Holidays
        elif 'promo' in query_lower or 'promotion' in query_lower or 'holiday' in query_lower:
            date_col = self.analyzer.date_columns[0] if self.analyzer.date_columns else None
            promo_col = None
            for col in self.analyzer.df.columns:
                if 'promo' in col.lower() or 'promotion' in col.lower():
                    promo_col = col
                    break
            holiday_col = None
            for col in self.analyzer.df.columns:
                if 'holiday' in col.lower():
                    holiday_col = col
                    break
            if promo_col:
                promo_sales = self.analyzer.df[self.analyzer.df[promo_col] == 1]['Order_Demand'].sum()
                nonpromo_sales = self.analyzer.df[self.analyzer.df[promo_col] == 0]['Order_Demand'].sum()
                return f"Sales with promo: {promo_sales}, without promo: {nonpromo_sales}"
            elif holiday_col:
                holiday_sales = self.analyzer.df[self.analyzer.df[holiday_col] == 1]['Order_Demand'].sum()
                nonholiday_sales = self.analyzer.df[self.analyzer.df[holiday_col] == 0]['Order_Demand'].sum()
                return f"Sales on holidays: {holiday_sales}, on non-holidays: {nonholiday_sales}"
            else:
                return "No promo or holiday column found in the dataset."

        # 7. Revenue & Pricing
        elif 'revenue' in query_lower or 'income' in query_lower:
            price_col = None
            for col in self.analyzer.df.columns:
                if 'price' in col.lower():
                    price_col = col
                    break
            if price_col and 'Order_Demand' in self.analyzer.df.columns:
                self.analyzer.df['revenue'] = self.analyzer.df[price_col] * self.analyzer.df['Order_Demand']
                total_revenue = self.analyzer.df['revenue'].sum()
                return f"Total revenue: {total_revenue:,.2f}"
            else:
                return "No price or order demand column found for revenue calculation."
        elif 'average price' in query_lower or 'avg price' in query_lower:
            price_col = None
            for col in self.analyzer.df.columns:
                if 'price' in col.lower():
                    price_col = col
                    break
            if price_col:
                avg_price = self.analyzer.df[price_col].mean()
                return f"Average price: {avg_price:,.2f}"
            else:
                return "No price column found in the dataset."

        # 8. Customer & Order Insights
        elif 'unique customer' in query_lower or 'customer count' in query_lower:
            customer_col = None
            for col in self.analyzer.df.columns:
                if 'customer' in col.lower():
                    customer_col = col
                    break
            if customer_col:
                unique_customers = self.analyzer.df[customer_col].nunique()
                return f"Number of unique customers: {unique_customers}"
            else:
                return "No customer column found in the dataset."
        elif 'average order' in query_lower or 'avg order' in query_lower:
            if 'Order_Demand' in self.analyzer.df.columns:
                avg_order = self.analyzer.df['Order_Demand'].mean()
                return f"Average order demand per transaction: {avg_order:,.2f}"
            else:
                return "No order demand column found in the dataset."

        # 9. Warehouse & Logistics
        elif 'warehouse' in query_lower:
            warehouse_col = None
            for col in self.analyzer.df.columns:
                if 'warehouse' in col.lower():
                    warehouse_col = col
                    break
            if warehouse_col and 'Order_Demand' in self.analyzer.df.columns:
                warehouse_sales = self.analyzer.df.groupby(warehouse_col)['Order_Demand'].sum().sort_values(ascending=False)
                return f"Order demand by warehouse: {warehouse_sales.to_dict()}"
            else:
                return "No warehouse or order demand column found in the dataset."
        elif 'delay' in query_lower or 'late' in query_lower:
            delay_col = None
            for col in self.analyzer.df.columns:
                if 'delay' in col.lower() or 'late' in col.lower():
                    delay_col = col
                    break
            if delay_col:
                delayed_orders = self.analyzer.df[self.analyzer.df[delay_col] == 1]
                return f"Number of delayed orders: {len(delayed_orders)}"
            else:
                return "No delay column found in the dataset."

        # 10. Comparisons & Rankings
        elif 'compare' in query_lower:
            product_ids = re.findall(r'\b\d+\b', query)
            if len(product_ids) >= 2 and 'Order_Demand' in self.analyzer.df.columns:
                sales = {}
                for pid in product_ids[:2]:
                    sales[pid] = self.analyzer.df[self.analyzer.df['Product_id'].astype(str) == pid]['Order_Demand'].sum()
                return f"Order demand comparison: {sales}"
            else:
                return "Please specify two product IDs to compare."

        # 11. Operational Metrics
        elif 'fulfillment rate' in query_lower:
            fulfill_col = None
            for col in self.analyzer.df.columns:
                if 'fulfill' in col.lower():
                    fulfill_col = col
                    break
            if fulfill_col:
                total_orders = len(self.analyzer.df)
                fulfilled = self.analyzer.df[self.analyzer.df[fulfill_col] == 1]
                rate = len(fulfilled) / total_orders if total_orders > 0 else 0
                return f"Order fulfillment rate: {rate:.2%}"
            else:
                return "No fulfillment column found in the dataset."
        elif 'return rate' in query_lower:
            return_col = None
            for col in self.analyzer.df.columns:
                if 'return' in col.lower():
                    return_col = col
                    break
            if return_col:
                total_orders = len(self.analyzer.df)
                returned = self.analyzer.df[self.analyzer.df[return_col] == 1]
                rate = len(returned) / total_orders if total_orders > 0 else 0
                return f"Order return rate: {rate:.2%}"
            else:
                return "No return column found in the dataset."

        # 12. General Data Exploration
        elif 'column' in query_lower or 'field' in query_lower:
            return f"Columns in dataset: {list(self.analyzer.df.columns)}"
        elif 'summary' in query_lower or 'overview' in query_lower:
            summary = self.analyzer.get_sales_summary()
            return f"Dataset Summary:\n- Total records: {summary['total_records']}\n- Date range: {summary['date_range']}\n- Numeric columns: {summary['numeric_columns']}"
        
        # 13. forecast (ARIMA)
        elif ('forecast' in query_lower or 'predict' in query_lower or 'likely to sell best' in query_lower) and ('product' in query_lower or 'produk' in query_lower):
            try:
                from statsmodels.tsa.arima.model import ARIMA
            except ImportError:
                return "statsmodels is required for ARIMA forecasting. Please install it with 'pip install statsmodels'."
            date_col = self.analyzer.date_columns[0] if self.analyzer.date_columns else None
            if not date_col or 'Product_id' not in self.analyzer.df.columns or 'Order_Demand' not in self.analyzer.df.columns:
                return "Dataset must have 'Product_id', 'Order_Demand', and a date column for forecasting."
            df = self.analyzer.df.copy()
            df['year'] = df[date_col].dt.year
            df['month'] = df[date_col].dt.month
            monthly = df.groupby(['Product_id', 'year', 'month'])['Order_Demand'].sum().reset_index()
            last_year = monthly['year'].max()
            last_month = monthly[monthly['year'] == last_year]['month'].max()
            
            if last_month == 12:
                forecast_year = last_year + 1
                forecast_month = 1
            else:
                forecast_year = last_year
                forecast_month = last_month + 1
            forecast = {}
            for pid in monthly['Product_id'].unique():
                prod_data = monthly[monthly['Product_id'] == pid].sort_values(['year', 'month'])
                y = prod_data['Order_Demand'].values
                if len(y) > 3: 
                    try:
                        model = ARIMA(y, order=(1,1,1))
                        model_fit = model.fit()
                        yhat = model_fit.forecast()[0]
                        forecast[pid] = yhat
                    except Exception as e:
                        continue
            if not forecast:
                return "Not enough data to forecast with ARIMA."
            best_pid = max(forecast, key=forecast.get)
            return f"ARIMA Forecast: Product {best_pid} is likely to sell best in {forecast_year}-{forecast_month:02d} (predicted demand: {forecast[best_pid]:.0f})"

        # 14. default
        else:
            context = f"Dataset has {len(self.analyzer.df)} records with columns: {list(self.analyzer.df.columns)}"
            return self.chatbot.generate_response(query, context)

def preprocess_data(df):
    df_processed = df.copy()
    
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    for col in date_columns:
        try:
            df_processed[col] = pd.to_datetime(df_processed[col])
        except:
            pass
    
    return df_processed

def main():
    print("Retail Data Analysis Chatbot")
    print("=" * 50)
    
    try:
        print("Loading dataset...")
        df = pd.read_csv('/Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm/retail_data/Sheet1-1-Retail_Dataset2.csv')
        df_processed = preprocess_data(df)
        print(f"Dataset loaded successfully! Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    analyzer = RetailAnalyzer(df_processed)
    chatbot = OllamaChatbot()
    query_processor = QueryProcessor(analyzer, chatbot)
    
    print("\nChatbot initialized! You can ask questions about the retail data.")
    print("=" * 50)
    
    while True:
        try:
            query = input("\n🤖 Ask a question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not query:
                continue
            
            print(f"\nProcessing")
            
            response = query_processor.process_query(query)
            print(f"\n🗣️ Response:\n{response}")
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 