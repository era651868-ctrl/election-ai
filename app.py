import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# 1. SET CONFIG FIRST
st.set_page_config(page_title="DemocracyFlow AI", page_icon="🗳️")

# 2. AUTH & VERTEX INIT
if os.path.exists("key.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

try:
    vertexai.init(project="election-assistant-495111", location="us-central1")
    @st.cache_resource
    def load_ai():
        return GenerativeModel("gemini-2.5-flash")
    model = load_ai()
except:
    st.warning("AI is initializing...")

# 3. SIDEBAR NAVIGATION (Restoring Features)
st.sidebar.title("🗳️ Menu")
page = st.sidebar.radio("Go to:", ["🏠 Dashboard", "📖 Voter Guide", "✅ Quiz", "🤖 AI Assistant"])

# 4. PAGE LOGIC
if page == "🏠 Dashboard":
    st.title("Election 2026 Readiness")
    st.metric("Voter Status", "ELIGIBLE", "18+")
    st.info("Goal: Become a Top Performer in Election Awareness.")
    st.progress(65)

elif page == "📖 Voter Guide":
    st.title("Step-by-Step Guide")
    st.write("1. Check ID")
    st.write("2. Ink Finger")
    st.write("3. Press the Blue Button")

elif page == "✅ Quiz":
    st.title("Knowledge Check")
    ans = st.radio("Which button records your vote?", ["Red", "Green", "Blue"])
    if st.button("Check Answer"):
        if ans == "Blue":
            st.success("Correct!")
            st.balloons()
        else:
            st.error("Try again!")

elif page == "🤖 AI Assistant":
    st.title("🤖 AI Assistant")
    q = st.text_input("Ask a question:")
    if q:
        with st.spinner("Processing..."):
            res = model.generate_content(q)
            st.write(res.text)
            
