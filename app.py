import os
import streamlit as st
from openai import OpenAI
from tools import get_current_time, get_city_weather, get_user_city, calculate

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant")

# API Key check (Streamlit secrets ya Environment variable se)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Please set GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

# Groq Client setup (OpenAI compatible)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input handling
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="qwen-2.5-32b", # ya mixtral-8x7b-32768 / llama-3.3-70b-versatile
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message.content
        st.markdown(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})