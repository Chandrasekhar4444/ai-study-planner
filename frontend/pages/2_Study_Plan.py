import streamlit as st
import requests

st.set_page_config(page_title="Study Plan", page_icon="📅")
st.title("📅 AI Study Planner")
st.write("Enter your subjects and schedule — the AI agent will create a personalized plan.")

API_URL = "http://localhost:8000"

with st.form("planner_form"):
    subjects = st.text_input("📚 Subjects (comma-separated)", placeholder="e.g. Python, Machine Learning, Statistics")
    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("📆 Number of Days", 1, 30, 7)
    with col2:
        hours = st.slider("⏱️ Hours Per Day", 1, 12, 3)
    submitted = st.form_submit_button("🤖 Generate Study Plan", use_container_width=True)

if submitted and subjects:
    with st.spinner("AI agent is creating your personalized study plan..."):
        try:
            response = requests.post(f"{API_URL}/plan", json={
                "subjects": subjects,
                "days": days,
                "hours_per_day": hours
            })
            if response.status_code == 200:
                plan = response.json()["plan"]
                st.session_state.study_plan = plan
                st.success("✅ Study plan generated!")
                st.markdown("---")
                st.markdown("### 📋 Your Personalized Study Plan")
                st.markdown(plan)
            else:
                st.error("Failed to generate plan.")
        except Exception as e:
            st.error(f"Backend not reachable: {e}")

elif st.session_state.get("study_plan"):
    st.markdown("### 📋 Your Last Study Plan")
    st.markdown(st.session_state.study_plan)