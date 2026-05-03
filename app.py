import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# --- 1. SECURITY & IDENTITY ---
# This uses the key.json file you uploaded to identify your app
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
vertexai.init(project="election-assistant-495111", location="us-central1")

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DemocracyFlow AI | Election 2026",
    page_icon="🗳️",
    layout="wide"
)

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 25px; background-image: linear-gradient(to right, #1e3c72 0%, #2a5298 100%); color: white; border: none; }
    .highlight-box { padding: 20px; border-radius: 10px; border-left: 5px solid #2a5298; background-color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Session State for Progress
if 'prog' not in st.session_state:
    st.session_state.prog = 65

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/voting-booth.png", width=80)
    st.title("DemocracyFlow AI")
    st.markdown("---")
    page = st.radio("Selection Menu", ["🏠 Home Dashboard", "📖 Voter Education", "✅ Knowledge Check", "🤖 AI Assistant"])
    st.markdown("---")
    st.write(f"**Voter Preparation:** {st.session_state.prog}%")
    st.progress(st.session_state.prog)

# --- 4. HOME DASHBOARD ---
if page == "🏠 Home Dashboard":
    st.title("🗳️ Election 2026: Readiness Portal")
    st.info("Your guide to participating in the world's largest democratic exercise.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Voting Age", "18+", "Eligible")
    m2.metric("Verification", "VVPAT", "Secured")
    m3.metric("System", "EVM", "Electronic")

    st.subheader("Your Preparation Status")
    if st.session_state.prog < 100:
        st.warning("Action Required: Complete the AI Assistant module to hit 100%.")
    else:
        st.success("🎯 Preparation 100% Complete. You are an Elite Voter.")

# --- 5. VOTER EDUCATION ---
elif page == "📖 Voter Education":
    st.title("The Voting Process")
    st.markdown("""
    <div class="highlight-box">
    <h4>Step 1: The Identity Check</h4>
    <p>Present your Voter ID or Aadhaar card to the First Polling Officer.</p>
    </div>
    <div class="highlight-box">
    <h4>Step 2: Marking & Registering</h4>
    <p>The Second Officer marks your finger with indelible ink.</p>
    </div>
    <div class="highlight-box">
    <h4>Step 3: Casting the Vote</h4>
    <p>Inside the booth, press the <b>blue button</b> on the EVM next to your candidate.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. KNOWLEDGE CHECK ---
elif page == "✅ Knowledge Check":
    st.title("Voter IQ Test")
    q1 = st.radio("What color button do you press on the EVM?", ["Red", "Blue", "Green"])
    q2 = st.selectbox("How long does the VVPAT slip stay visible?", ["3 Seconds", "7 Seconds", "10 Seconds"])

    if st.button("Finalize My Score"):
        if q1 == "Blue" and q2 == "7 Seconds":
            st.balloons()
            st.success("Perfect Score! You understand the protocol.")
        else:
            st.warning("Check your answers and try again!")

# --- 7. AI ASSISTANT ---
elif page == "🤖 AI Assistant":
    st.title("🤖 Ask DemocracyFlow AI")
    st.write("Verified Insights via Gemini 2.5 Flash (Vertex AI).")
    
    user_query = st.text_input("Ask a question about election rules:")
    
    if user_query:
        with st.spinner("Analyzing Election Protocols..."):
            try:
                # Using the latest Gemini 2.5 model name we set earlier
                model = GenerativeModel("gemini-2.5-flash")
                
                prompt = f"Answer briefly: {user_query}. At the end, MUST add: 'For official verification, visit https://eci.gov.in'"
                response = model.generate_content(prompt)
                
                st.session_state.prog = 100
                st.success("Analysis Complete")
                st.markdown(f"**AI Response:**\n\n{response.text}")
                
                st.divider()
                st.balloons()
                st.info("🎯 **100% COMPLETE!** Your preparation is finished.")
            except Exception as e:
                st.error(f"Error: {e}")
    
