import streamlit as st

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧠 AI Study Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI-powered learning companion with RAG + Agentic AI</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">📄</div>
        <b>Upload Notes</b>
        <p>Upload your PDFs and study materials</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">📅</div>
        <b>AI Study Plan</b>
        <p>Get a personalized day-wise schedule</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">💬</div>
        <b>Ask AI</b>
        <p>Ask questions from your notes using RAG</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">🧪</div>
        <b>AI Quiz</b>
        <p>Test yourself with auto-generated quizzes</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("👈 Use the sidebar to navigate between pages. Start by uploading your study material!")

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}
if "study_plan" not in st.session_state:
    st.session_state.study_plan = ""