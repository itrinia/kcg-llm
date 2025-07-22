import sqlite3
import pandas as pd

# Open the connection
conn = sqlite3.connect("/Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm/retail_data/agent/retail_sales.db")

# Read the 'sales' table into a DataFrame
df = pd.read_sql_query("SELECT * FROM sales", conn)

# Show the first 5 rows
print(df.head(100))

# Close the connection
conn.close()