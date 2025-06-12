import pandas as pd
import sqlite3

# Step 1: Load the CSV file
csv_path = r"C:\Users\ValuriCrishna\Downloads\archive\BankChurners.csv"
df = pd.read_csv(csv_path)  # Use read_csv for .csv files

# Step 2: Inspect (optional)
print("Columns:", df.columns.tolist())
print("Sample:", df.head())

# Step 3: Create SQLite DB and write the data
db_path = "bank_customers.db"
table_name = "customers"

conn = sqlite3.connect(db_path)
df.to_sql(table_name, conn, if_exists="replace", index=False)
conn.close()
