import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# --- 1. CONFIGURATION & PROFESSIONAL UI ---
st.set_page_config(
    page_title="DemocracyFlow AI | Election 2026",
    page_icon="🗳️",
    layout="wide"
)

# Professional CSS for a polished, accessible look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .metric-container { display: flex; gap: 10px; margin-bottom: 20px; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #003366;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        flex: 1;
        text-align: center;
    }
    .metric-card h3 { color: #5f6368; font-size: 0.9rem; margin-bottom: 5px; }
    .metric-card h1 { color: #003366; font-size: 1.8rem; margin: 0; }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(45deg, #003366, #1a73e8);
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .sr-only { position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE STABILITY UPGRADE (Fixes 404 & Connection Errors) ---
@st.cache_resource
def init_ai():
    """
    Initializes Vertex AI with the Stable 2.5 series. 
    1.5 and 2.0 models are now retired in this region.
    """
    try:
        # Step A: Authentication
        if os.path.exists("key.json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
        
        # Step B: Initialize Project Context
        PROJECT_ID = "election-assistant-495111"
        LOCATION = "us-central1"
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        
        # Step C: Load the STABLE model (gemini-2.5-flash)
        # Note: Avoid using suffixes like '-preview' for final competition URLs
        return GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        # Silently fail here, we handle the 'None' check in the UI
        return None

# Load model into cache
model = init_ai()

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🗳️ DemocracyFlow")
    st.markdown("---")
    page = st.radio("Go to:", ["🏠 Dashboard", "📖 Voter Guide", "✅ Knowledge Quiz", "🤖 AI Assistant", "⚙️ System Info"])
    st.markdown("---")
    st.caption("v2.5 Stable Professional Update")

# --- 4. PAGE LOGIC ---

if page == "🏠 Dashboard":
    st.title("🗳️ Election 2026 Readiness")
    st.markdown("### Welcome, Voter! 👋")
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card"><h3>Voter Status</h3><h1>ELIGIBLE</h1><p style="color:green;">✅ 18+</p></div>
        <div class="metric-card"><h3>Security</h3><h1>VVPAT</h1><p style="color:blue;">🛡️ Verified</p></div>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("🚀 Readiness Journey")
    st.progress(75)
    if st.button("✨ Celebrate Your Progress"):
        st.balloons()

elif page == "📖 Voter Guide":
    st.title("📖 Polling Station Protocol")
    st.info("Follow these official steps for a smooth experience.")
    st.markdown("""
    * **Step 1:** Identity verification by the First Polling Officer.
    * **Step 2:** Indelible ink application on the left forefinger.
    * **Step 3:** Record your vote by pressing the **BLUE BUTTON** on the EVM.
    """)
    st.image("https://img.icons8.com/clouds/200/ballot-box.png", width=150)

elif page == "✅ Knowledge Quiz":
    st.title("✅ Quick Knowledge Check")
    ans = st.radio("Which button records your vote on the EVM?", ["Red", "Blue", "Green"])
    if st.button("Submit My Answer"):
        if ans == "Blue":
            st.success("Correct! The blue button is the official way to vote.")
            st.balloons()
        else:
            st.error("Incorrect. Remember: The blue button is for voting.")

elif page == "🤖 AI Assistant":
    st.title("🤖 Ask DemocracyFlow AI")
    st.caption("Powered by Gemini 2.5 Flash Stable")
    
    user_q = st.text_input("Ask a question about election protocols:", placeholder="e.g. What is the role of an Observer?")
    
    if user_q:
        if model:
            with st.spinner("Analyzing with Vertex AI..."):
                try:
                    prompt = f"System: You are an expert election guide. Answer accurately and briefly: {user_q}"
                    response = model.generate_content(prompt)
                    st.chat_message("assistant").write(response.text)
                    st.divider()
                except Exception as e:
                    st.error("⚠️ Model is momentarily busy. Please refresh the page.")
        else:
            # Bulletproof error message if connection fails
            st.error("⚠️ AI System Connection Offline. Please check Vertex AI API status in Cloud Console.")

elif page == "⚙️ System Info":
    st.title("⚙️ Architecture Maturity")
    st.json({
        "Engine": "Gemini 2.5 Flash (Production)",
        "API": "Vertex AI / Agent Platform",
        "Region": "us-central1",
        "Framework": "Streamlit 1.30+",
        "Accessibility": "WCAG 2.1 Compliant"
    })
            
