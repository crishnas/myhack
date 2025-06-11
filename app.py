import streamlit as st
import pandas as pd
import requests

# Ollama config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "meta-Llama-3.1-8B-instruct_f32:latest"

# Prompt generator
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

# Streamlit UI
st.title("🧠 LLM Sentiment Analyzer (Ollama + Streamlit)")

uploaded_file = st.file_uploader("📤 Upload CSV file", type=["csv"])
text_column = st.text_input("📝 Enter the column name containing text", value="text")

if uploaded_file and text_column:
    try:
        df = pd.read_csv(uploaded_file)
        if text_column not in df.columns:
            st.error(f"Column '{text_column}' not found in uploaded file.")
        else:
            st.info("🔄 Analyzing sentiments using LLM...")
            with st.spinner("Processing..."):
                df["llm_sentiment"] = df[text_column].apply(
                    lambda x: query_ollama(generate_prompt(str(x)))
                )
            st.success("✅ Sentiment classification complete!")

            st.subheader("📈 Result Preview")
            st.dataframe(df.head())

            csv_output = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Results as CSV",
                data=csv_output,
                file_name="output_llm_sentiment.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Failed to process the file: {e}")
