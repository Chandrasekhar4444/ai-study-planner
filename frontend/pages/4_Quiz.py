import streamlit as st
import requests

st.set_page_config(page_title="AI Quiz", page_icon="🧪")
st.title("🧪 AI Quiz Generator")
st.write("Test your knowledge with AI-generated questions from your study material.")

API_URL = "http://localhost:8000"

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

with st.form("quiz_form"):
    topic = st.text_input("📖 Topic to quiz on", placeholder="e.g. Machine Learning, Neural Networks")
    num_q = st.slider("Number of Questions", 3, 10, 5)
    gen = st.form_submit_button("🤖 Generate Quiz", use_container_width=True)

if gen and topic:
    with st.spinner("AI is generating your quiz..."):
        try:
            response = requests.post(f"{API_URL}/quiz", json={"topic": topic, "num_questions": num_q})
            if response.status_code == 200:
                st.session_state.quiz_data = response.json()["questions"]
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}
            else:
                st.error("Failed to generate quiz.")
        except Exception as e:
            st.error(f"Backend error: {e}")

if st.session_state.quiz_data and not st.session_state.quiz_submitted:
    st.markdown("---")
    st.markdown("### Answer the Questions:")
    with st.form("answer_form"):
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            st.session_state.user_answers[i] = st.radio(
                f"Select answer for Q{i+1}",
                q["options"],
                key=f"q_{i}",
                label_visibility="collapsed"
            )
            st.markdown("")
        submit_quiz = st.form_submit_button("✅ Submit Quiz", use_container_width=True)
    if submit_quiz:
        st.session_state.quiz_submitted = True
        st.rerun()

if st.session_state.quiz_submitted and st.session_state.quiz_data:
    st.markdown("---")
    st.markdown("### 📊 Quiz Results")
    score = 0
    for i, q in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers.get(i, "")
        correct = user_ans == q["answer"]
        if correct:
            score += 1
            st.success(f"Q{i+1}: ✅ Correct! — {q['question']}")
        else:
            st.error(f"Q{i+1}: ❌ Wrong — Correct: {q['answer']}")
        with st.expander(f"Explanation for Q{i+1}"):
            st.write(q.get("explanation", "No explanation provided."))

    pct = round((score / len(st.session_state.quiz_data)) * 100)
    st.markdown(f"### 🎯 Score: {score}/{len(st.session_state.quiz_data)} ({pct}%)")

    if pct >= 80:
        st.balloons()
        st.success("🌟 Excellent! You're well prepared!")
    elif pct >= 50:
        st.warning("📚 Good effort! Review the wrong answers.")
    else:
        st.error("📖 Keep studying! Try again after reviewing the material.")

    st.session_state.quiz_scores[f"Quiz {len(st.session_state.quiz_scores)+1}"] = pct