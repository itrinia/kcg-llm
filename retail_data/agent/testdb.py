import sqlite3
conn = sqlite3.connect('/Users/ileene/Library/CloudStorage/OneDrive-UniversitasCiputra/kcg/kcg-llm/retail_data/dataset/retail_sales.db')
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())