import sqlite3
import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
import re


def create_agent():
    try:
        llm = OllamaLLM(model="deepseek-r1:1.5b", streaming=True)
        db = SQLDatabase.from_uri("sqlite:////Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm/retail_data/dataset/retail_sales.db")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            template="""
You are a helpful assistant. Answer the user's SQL question using the database.
Return ONLY the final answer as a single number or word, with NO explanation, NO code, and NO tags.
Do NOT include any reasoning, SQL code, or markdown formatting.
Just output the answer as plain text, for example: 1234

Available tools: {tools}
Tool names: {tool_names}

Question: {input}
{agent_scratchpad}
"""
        )

        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            prompt=prompt,
            verbose=False,
            max_iterations=15,
            max_execution_time=120,
            handle_parsing_errors=True
        )
        return agent_executor
    except Exception as e:
        print(f"✗ Error creating agent: {e}")
        return None

def main():
    print("=" * 60)
    print("RETAIL DATA CHATBOT")
    print("=" * 60)
    print("Type 'q' to end the session")
    print("=" * 60)
    

    
    # Create agent
    agent = create_agent()
    if agent is None:
        return
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['q']:
                print("\nThanks")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Handle greetings and non-SQL input
            if user_input.lower() in ['hi', 'hello', 'hey']:
                print("\nBot: Hello! Please ask a question about the retail sales data.")
                continue

            # Handle help/columns command
            if user_input.lower() in ['help', 'columns']:
                print("\nBot: Retail Dataset Columns and Descriptions:")
                print("- Product_id: Unique identifier for each product")
                print("- Product_Code: Code for the product")
                print("- Warehouse: Warehouse location")
                print("- Product_Category: Category of the product")
                print("- Date: Date of the record")
                print("- Order_Demand: Number of orders/demand for the product")
                print("- Open: Whether the store/warehouse was open (likely 1/0)")
                print("- Promo: Whether a promotion was active (likely 1/0)")
                print("- StateHoliday: Whether it was a state holiday (likely 1/0 or a string)")
                print("- SchoolHoliday: Whether it was a school holiday (likely 1/0)")
                print("- Petrol_price: Price of petrol on that date")
                continue

            # Get response from agent
            print("\nBot: Thinking...")
            output = ""
            for chunk in agent.stream({"input": user_input}):
                text = chunk.get('output', '')
                print(text, end='', flush=True)
                output += text
            print()  # Newline after streaming

            # Post-process to extract the answer
            match = re.search(r'\d+', output)
            if match:
                print(f"\nBot: {match.group(0)}")
            else:
                print(f"\nBot: {output}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Chatbot interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try asking your question in a different way.")

if __name__ == "__main__":
    main() 