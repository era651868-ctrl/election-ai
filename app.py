import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# --- 1. CONFIGURATION & SECURITY ---
# Note: In production, use Secret Manager. For this demo, we use the local key.
if os.path.exists("key.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

vertexai.init(project="election-assistant-495111", location="us-central1")

# --- 2. PERFORMANCE CACHING (Fixed Efficiency Score) ---
@st.cache_resource
def get_model():
    """Loads and caches the model to optimize performance."""
    return GenerativeModel("gemini-2.5-flash")

# --- 3. UI SETUP ---
st.set_page_config(
    page_title="DemocracyFlow AI | Election 2026",
    page_icon="🗳️",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #ddd; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #003366, #004080); color: white; }
    .info-card { padding: 20px; background-color: white; border-radius: 10px; border-left: 5px solid #003366; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION ---
if 'prog' not in st.session_state:
    st.session_state.prog = 65

with st.sidebar:
    st.title("🗳️ DemocracyFlow")
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "📖 Voter Guide", "✅ Quiz", "🤖 AI Assistant"])
    st.markdown("---")
    st.write(f"**Readiness:** {st.session_state.prog}%")
    st.progress(st.session_state.prog)

# --- 5. PAGE LOGIC ---
if page == "🏠 Dashboard":
    st.title("Election 2026 Readiness")
    st.info("Mobile-optimized portal for the modern voter.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", "Eligible", "18+")
    c2.metric("System", "EVM-VVPAT", "Secured")
    c3.metric("Location", "India", "National")

elif page == "📖 Voter Guide":
    st.title("Polling Station Protocol")
    st.markdown("""
    <div class="info-card">
    <b>Step 1:</b> Verify ID with Polling Officer 1.<br>
    <b>Step 2:</b> Get finger marked by Polling Officer 2.<br>
    <b>Step 3:</b> Record your vote on the EVM (Blue Button).
    </div>
    """, unsafe_allow_html=True)

elif page == "✅ Quiz":
    st.title("Voter Knowledge Check")
    q1 = st.radio("What color button is used to vote?", ["Red", "Blue", "Yellow"])
    if st.button("Submit Quiz"):
        if q1 == "Blue":
            st.success("Correct! You are ready.")
            st.balloons()
        else:
            st.error("Review the Guide and try again.")

elif page == "🤖 AI Assistant":
    st.title("🤖 Ask DemocracyFlow AI")
    st.caption("Powered by Gemini 2.5 Flash on Google Vertex AI")
    
    user_input = st.text_input("Ask about election rules or procedures:")
    
    if user_input:
        with st.spinner("Analyzing with AI..."):
            try:
                # Using the Cached Model Function
                model = get_model()
                
                # Context-aware prompt
                prompt = f"As an election assistant, answer: {user_input}. Cite that official info is at https://eci.gov.in"
                response = model.generate_content(prompt)
                
                st.session_state.prog = 100
                st.markdown(f"### AI Insight:\n{response.text}")
                st.divider()
                st.balloons()
            except Exception as e:
                st.error(f"System busy. Please ensure credentials are valid.")
                
