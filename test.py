import streamlit as st
import requests
import json

# 🔧 Set your OpenRouter API key and model
API_KEY = "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"
MODEL_NAME = "mistralai/mistral-7b-instruct"  # or "mistralai/mistral-7b-instruct", "meta-llama/Meta-Llama-3-8B-Instruct"

# UI
st.set_page_config(page_title="ChatGPT via OpenRouter", layout="centered")
st.title("🧠 Chat with OpenRouter LLM")
st.caption("Powered by OpenRouter API")

# Store messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show previous messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Ask something...")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call OpenRouter API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                        "X-Title": "streamlit-chat",  # Optional for OpenRouter rankings
                    },
                    data=json.dumps({
                        "model": MODEL_NAME,
                        "messages": st.session_state.chat_history
                    })
                )
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"❌ Error: {e}"

            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
