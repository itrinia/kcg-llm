import sqlite3
import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
import re

# def setup_database():
#     try:
#         df = pd.read_csv("Sheet1-1-Retail_Dataset2.csv")
#         conn = sqlite3.connect("retail_sales.db")
#         df.to_sql("sales", conn, if_exists="replace", index=False)
#         conn.close()
#         print("✓ Database loaded successfully!")
#         return True
#     except FileNotFoundError:
#         print("✗ Error: Sheet1-1-Retail_Dataset2.csv not found!")
#         return False
#     except Exception as e:
#         print(f"✗ Error loading database: {e}")
#         return False

def create_agent():
    try:
        llm = OllamaLLM(model="mistral")
        db = SQLDatabase.from_uri("sqlite:///retail_sales.db")
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
    
    # # Setup database
    # if not setup_database():
    #     return
    
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
            
            # Get response from agent
            print("\nBot: Thinking...")
            response = agent.invoke({"input": user_input})
            
            # Display response
            output = response['output']
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