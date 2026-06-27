import streamlit as st
import requests

st.set_page_config(page_title="Upload Notes", page_icon="📄")
st.title("📄 Upload Study Material")
st.write("Upload your PDF notes — the AI will read and index them for RAG.")

API_URL = "http://localhost:8000"

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    st.info(f"File selected: **{uploaded_file.name}**")
    if st.button("📤 Upload & Process", use_container_width=True):
        with st.spinner("Uploading and embedding document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    data = response.json()
                    st.success(data["message"])
                    if "uploaded_files" not in st.session_state:
                        st.session_state.uploaded_files = []
                    st.session_state.uploaded_files.append(uploaded_file.name)
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Cannot connect to backend. Make sure FastAPI is running.\nError: {e}")

if st.session_state.get("uploaded_files"):
    st.markdown("### ✅ Uploaded Files")
    for f in st.session_state.uploaded_files:
        st.markdown(f"- 📄 {f}")