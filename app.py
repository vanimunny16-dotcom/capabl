import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        api_key = ""

os.environ["GOOGLE_API_KEY"] = api_key

st.set_page_config(page_title="Saksham HR Agent | Resume Matcher", layout="wide", page_icon="💼")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); font-family: 'Inter', sans-serif; }
    .header-card { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-card"><h2 style="color:#fff;margin:0;">💼 Saksham HR Agent — Resume & Candidate Matcher</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📄 Candidate Resume Text")
    resume_text = st.text_area("Paste Candidate Resume / Skills profile here:", height=200)
    job_desc = st.text_input("Target Job Role (e.g., Python Developer / Data Analyst):")
    
    if st.button("⚡ Evaluate Match Score", type="primary"):
        if not resume_text or not job_desc:
            st.warning("Please provide both resume text and target job role.")
        else:
            with st.spinner("Analyzing candidate profile fit..."):
                prompt = f"Evaluate this resume for the role '{job_desc}'.\nResume:\n{resume_text}\n\nProvide:\n1. Match Score (%)\n2. Key Strengths\n3. Skill Gaps\n4. Recommendation."
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=api_key, temperature=0.2)
                    res = llm.invoke(prompt)
                    st.success("Analysis Complete!")
                    st.markdown(res.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with col2:
    st.subheader("💬 HR & Career Assistant")
    if "hr_chat" not in st.session_state: st.session_state.hr_chat = []
    
    for m in st.session_state.hr_chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])
        
    if q := st.chat_input("Ask HR questions (e.g., 'How do I optimize my resume for ATS?')"):
        st.session_state.hr_chat.append({"role": "user", "content": q})
        with st.chat_message("user"): st.markdown(q)
        
        with st.chat_message("assistant"):
            try:
                llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=api_key, temperature=0.3)
                res = llm.invoke(f"You are an expert HR Agent. Answer concisely: {q}")
                ans = res.content
            except Exception as e:
                ans = f"Error: {str(e)}"
            st.markdown(ans)
            st.session_state.hr_chat.append({"role": "assistant", "content": ans})
