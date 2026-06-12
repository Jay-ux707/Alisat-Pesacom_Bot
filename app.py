import streamlit as st
import requests
import json

# Set up page config and brand coloring
st.set_page_config(page_title="PESACOM AI Assistant", page_icon="💼", layout="centered")

# Custom CSS to inject your JI brand styling (#19-4914)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b2209; /* Dark variation of your brand color */
        color: #ffffff;
    }
    h1 {
        color: #194914 !important;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("JI Operations & Dev Assistant")
st.write("Managing PESACOM Finance & Software Engineering Projects.")

# Hardcoded API Details
API_KEY = "AQ.Ab8RN6LPpJgJvcG-2B-MrJJQZtJsQjELAl8zyrje-HXKTShGwAn"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

SYSTEM_INSTRUCTION = """
You are the official Digital Operations Manager for PESACOM Finance, based in Uganda. 
You represent the brand 'JI' (Jay Kimari). Your goal is to provide elite service and maintain absolute professionalism.

- BRAND IDENTITY: Your color palette is #19-4914. Your tone is warm, authoritative, and efficient.
- OPERATIONAL SCOPE: You specialize in microfinance, loans, and financial advice. 
- LEGAL COMPLIANCE: All advice regarding loans, interest, and lending must strictly align with the 'Tier 4 Microfinance Institutions and Money Lenders Act 2016' of Uganda.
- MODES:
    1. [DEV]: You are an expert software engineer. Write clean, modular Python/JS code for Jay's personal projects.
    2. [BIZ]: You are a Business Assistant for PESACOM Finance. 
       - Always verify if a client has their proper documentation.
       - Use the 'Human Handoff' protocol: If a query involves complex loan approval or legal liability, state: 'To ensure your security and compliance, I am escalating this to our senior management team for review.'
- RULES: Never guess regarding legal/financial status. When in doubt, prioritize formal procedure over speed.
"""

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_history" not in st.session_state:
    st.session_state.api_history = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask [DEV] for code or [BIZ] for business help..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.api_history.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {
        "contents": st.session_state.api_history,
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "generationConfig": {"temperature": 0.3}
    }
    headers = {"Content-Type": "application/json"}

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(URL, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    res_data = response.json()
                    bot_response = res_data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.session_state.api_history.append({"role": "model", "parts": [{"text": bot_response}]})
                else:
                    st.error(f"API Error ({response.status_code})")
            except Exception as e:
                st.error(f"Connection Error: {e}")
