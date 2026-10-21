import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant")

# Streamlit Secrets ya Environment variable se API key fetch ho jayegi
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY nahi mili! Streamlit Cloud ke Advanced Settings (Secrets) mein key add karein.")
    st.stop()

# Groq Client Initialization (OpenAI SDK ke sath compatible)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Chat history state initialize karein
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat history UI par show karein
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input text box
if prompt := st.chat_input("Ask me anything..."):
    # User ka message history mein append karein
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Groq API ko query bhein
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Ya "qwen-2.5-32b"
                messages=st.session_state.messages
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)
        
    # Assistant ka reply history mein save karein
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})