import streamlit as st
import sqlite3
import pandas as pd
import requests

# Ollama API config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "meta-Llama-3.1-8B-instruct_f32:latest"

# Prompt generation
def generate_prompt(text):
    return f"Classify the sentiment of the following text as Positive, Negative, or Neutral:\n\n{text}"

# Query Ollama API
def query_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"Error: {e}"

# SQLite interaction
def load_data_from_db(db_path, table_name, text_column):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT rowid AS id, * FROM {table_name}", conn)
    conn.close()
    return df

def save_results_to_db(db_path, table_name, df):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

# Streamlit UI
st.title("🧠 LLM Sentiment Analyzer (SQLite + Ollama)")

db_path = st.text_input("📂 Path to SQLite DB", value="sentiment.db")
table_name = st.text_input("📋 Table name", value="texts")
text_column = st.text_input("📝 Column with input text", value="text")

if st.button("Run Sentiment Analysis"):
    try:
        df = load_data_from_db(db_path, table_name, text_column)
        if text_column not in df.columns:
            st.error(f"Column '{text_column}' not found in table '{table_name}'.")
        else:
            st.info("🔄 Running sentiment analysis...")
            with st.spinner("Processing..."):
                df["llm_sentiment"] = df[text_column].apply(lambda x: query_ollama(generate_prompt(str(x))))
                save_results_to_db(db_path, f"{table_name}_with_sentiment", df)
            st.success(f"✅ Results saved to table: {table_name}_with_sentiment")

            st.subheader("📊 Preview")
            st.dataframe(df.head())

            # Optional CSV download
            csv_output = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Results as CSV",
                data=csv_output,
                file_name="llm_sentiment_output.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error: {e}")
