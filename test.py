import pandas as pd
import openai
from sqlalchemy import create_engine

openai.api_key = "YOUR_OPENAI_API_KEY"

def load_excel(file_path):
    df = pd.read_excel(file_path)
    return df

def load_db_table(conn_str, table_name, limit=1000):
    engine = create_engine(conn_str)
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    df = pd.read_sql(query, engine)
    return df

def ask_llm_about_data(df, user_query):
    # Sample 20 rows for token limits; change as needed
    sample = df.head(20).to_csv(index=False)
    prompt = (
        f"You are a senior data scientist.\n\n"
        f"User question: {user_query}\n\n"
        f"Here is a sample of the data (CSV):\n{sample}\n\n"
        f"If calculations are needed, show Python pandas code."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a senior data scientist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=1500
    )
    return response['choices'][0]['message']['content']

def main():
    print("\n=== LLM Data Analysis Tool ===\n")
    mode = input("Load data from (1) Excel or (2) Database? [1/2]: ").strip()
    if mode == "1":
        file_path = input("Enter Excel file path: ").strip()
        df = load_excel(file_path)
    elif mode == "2":
        print("\n--- Example: mysql+pymysql://user:password@host/db ---")
        conn_str = input("Enter SQLAlchemy connection string: ").strip()
        table_name = input("Enter table name: ").strip()
        df = load_db_table(conn_str, table_name)
    else:
        print("Invalid input.")
        return

    print(f"\nLoaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
    print("Columns:", df.columns.tolist())
    print("\nType your analysis questions (type 'exit' to quit):")

    while True:
        user_query = input("\nYou: ").strip()
        if user_query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        response = ask_llm_about_data(df, user_query)
        print("\n[LLM]:\n", response)

if __name__ == "__main__":
    main()
