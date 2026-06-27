import streamlit as st
import requests

st.set_page_config(page_title="Ask AI", page_icon="💬")
st.title("💬 Ask AI (RAG-Powered)")
st.write("Ask any question — the AI searches your uploaded notes to answer.")

API_URL = "http://localhost:8000"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question from your study material...")

if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your notes..."):
            try:
                response = requests.post(f"{API_URL}/ask", json={"question": question})
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                else:
                    st.error("Could not get an answer.")
            except Exception as e:
                st.error(f"Backend not reachable: {e}")