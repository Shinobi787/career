# app.py
import streamlit as st
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

st.set_page_config(page_title="AI Career Profile (BTS)", page_icon="🤖", layout="centered")

# Load OpenAI API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------- UI STYLE ----------------------
st.markdown("""
<style>
body {background-color: #f7f9fc;}
.report-box {
    background: white;
    padding: 25px;
    border-radius: 12px;
    border-left: 6px solid #4A90E2;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    font-size: 16px;
    line-height: 1.6;
}
.title {
    color: #4A90E2;
    font-size: 32px !important;
    font-weight: 700;
}
.sub {
    color: #555;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown("<h1 class='title'>🤖 AI Career Personality Test — BTS Edition</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Discover what AI can do in *your* role — smart, personalized, ROI-focused.</p>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------- FORM ----------------------
with st.form("career_form"):
    role = st.text_input("Your Role / Job Title")
    seniority = st.selectbox("Seniority / Decision Power", ["Student", "Individual Contributor", "Senior IC", "Manager", "Head / Director", "Founder / CXO"])
    team_size = st.text_input("Team Size You Influence (0 if none)", value="0")
    daily_tasks = st.text_area("Top 3 Daily Tasks (comma-separated)")
    kpis = st.text_input("Main KPIs or Goals")
    pain_point = st.text_input("Biggest repetitive/time-consuming task")
    ai_level = st.selectbox("AI Familiarity", ["Beginner", "Intermediate", "Advanced"])
    learn_style = st.selectbox("Preferred Learning Style", ["Practical projects", "Short videos", "Reading", "Hands-on"])
    time_per_week = st.selectbox("Time you can commit weekly", ["<3 hours", "3–5 hours", "6–8 hours", "8+ hours"])
    submit = st.form_submit_button("✨ Generate My AI Profile")

# ---------------------- BACKEND LOGIC ----------------------
if submit:
    if not role or not daily_tasks:
        st.warning("Please fill in at least your role and daily tasks.")
    else:
        with st.spinner("Generating your personalized AI profile…"):

            prompt = f"""
You are an expert career strategist + AI productivity mentor. 
Create a premium BTS-style “AI Career Profile” based on:

Role: {role}
Seniority: {seniority}
Team Size: {team_size}
Daily Tasks: {daily_tasks}
KPIs: {kpis}
Pain Point: {pain_point}
AI Level: {ai_level}
Learn Style: {learn_style}
Time Available: {time_per_week}

FOLLOW EXACT FORMAT:

1) 🎯 ONE-LINER SUMMARY  
2) 🎭 AI PERSONALITY TYPE + reason  
3) 🚀 TOP 3–5 USE CASES (each with WHAT + IMPACT + FIRST STEP)  
4) 💼 BUSINESS IMPACT & QUICK ROI  
5) 🧭 6-WEEK PERSONAL ROADMAP (1 line/week)  
6) 🛠 TOOL + ONE STARTER PROJECT  
7) 👥 TEAM PILOT PLAN (only if team_size > 0 or seniority in Manager/Head/Founder)  
8) 💬 PROOF LINE  
9) 👋 SOFT CTA  

Tone: sharp, professional, mobile-friendly, premium, no fluff.
Max 450 words.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=750,
                temperature=0.2
            )

            result = response.choices[0].message.content  # FIXED LINE

        # ---------------- UI OUTPUT ----------------
        st.markdown("### 🎉 Your Personalized AI Career Profile")
        st.markdown(f"<div class='report-box'>{result}</div>", unsafe_allow_html=True)

        # ------------- PDF GENERATION -------------
        def generate_pdf(text):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(temp_file.name, pagesize=letter)
            width, height = letter
            y = height - 50

            for line in text.split("\n"):
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(40, y, line[:110])
                y -= 18

            c.save()
            return temp_file.name

        pdf_file = generate_pdf(result)

        st.download_button(
            label="📄 Download AI Profile as PDF",
            data=open(pdf_file, "rb").read(),
            file_name="AI_Career_Profile.pdf",
            mime="application/pdf"
        )

        st.success("Your AI profile is ready! You can download the PDF or share it on WhatsApp.")
