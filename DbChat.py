import streamlit as st
import sqlite3
import pandas as pd
import requests
import json
import plotly.express as px
import re

# Configuration
DB_PATH = r"D:\myhack\myhack\bank_customers.db"
TABLE_NAME = "customers"
MODEL_NAME = "mistralai/mistral-7b-instruct"
API_KEY = "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"

# Clean text to remove special characters
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'[^\w\s]', '', text)
    return text

# Load data from SQLite
def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT rowid AS id, * FROM {TABLE_NAME}", conn)
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].map(clean_text)
        conn.close()
        st.success(f"✅ Loaded {len(df)} records from table '{TABLE_NAME}'.")
        return df
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

# Convert row to prompt string
def row_to_prompt(row: pd.Series):
    return "\n".join([f"{col}: {row[col]}" for col in row.index if col != "id"])

# Call OpenRouter LLM
def query_llm(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "X-Title": "db-nlp-app"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

# Initialize state
if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

# Page layout
st.set_page_config(layout="wide")
st.write("🔄 App loaded.")

left_col, right_col = st.columns([1, 3])

# Left sidebar - Prompt History
with left_col:
    st.subheader("📜 Recent Prompts")
    if st.session_state.prompt_history:
        for p in reversed(st.session_state.prompt_history[-10:]):
            st.markdown(f"- {p}")
    else:
        st.markdown("_No prompts yet._")

# Right main panel
with right_col:
    st.title("🤖 Customer NLP Chatbot")

    st.markdown("""
    **Examples**:
    - Classify this customer as High, Medium, or Low risk
    - Will this customer churn?
    - Summarize this customer's transaction behavior
    """)

    user_prompt = st.text_area("Enter your analysis prompt:", height=100)

    if st.button("💬 Run Prompt"):
        if not user_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            st.session_state.prompt_history.append(user_prompt.strip())
            df = load_data()

            if df.empty:
                st.warning("No data to process.")
            else:
                st.write("📦 Data shape:", df.shape)
                st.write("🔁 Sample input row:", row_to_prompt(df.iloc[0]))

                with st.spinner("Processing records through LLM..."):
                    df["llm_input"] = df.apply(row_to_prompt, axis=1)
                    df["llm_output"] = df["llm_input"].apply(lambda x: query_llm(f"{user_prompt}\n\n{x}"))

                st.success("✅ NLP analysis complete.")
                st.dataframe(df[["id", "llm_output"]])

                if st.checkbox("📈 Show Chart from Output"):
                    colname = st.selectbox("Group LLM output by:", options=["llm_output"])
                    chart_type = st.radio("Chart Type", ["Pie", "Bar"])

                    count_df = df[colname].value_counts().reset_index()
                    count_df.columns = ["label", "count"]

                    if chart_type == "Pie":
                        fig = px.pie(count_df, names="label", values="count", title="Pie Chart of LLM Output")
                    else:
                        fig = px.bar(count_df, x="label", y="count", title="Bar Chart of LLM Output")

                    st.plotly_chart(fig)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Results", csv, "nlp_result_full_table.csv", mime="text/csv")
