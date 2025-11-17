# app.py
import streamlit as st
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import tempfile
import re
import os

st.set_page_config(page_title="AI Career Profile (BTS)", page_icon="🤖", layout="centered")

# Load OpenAI API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------- UI STYLE ----------------------
st.markdown("""
<style>
body {background-color: #f7f9fc;}
.report-box {
    background: #ffffff;
    padding: 22px;
    border-radius: 12px;
    border-left: 6px solid #4A90E2;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
    font-size: 15px;
    line-height: 1.6;
    color: #111111;              /* EXPLICIT dark text color to avoid white-on-white */
    max-width: 900px;
}
.title {
    color: #1f6feb;
    font-size: 32px !important;
    font-weight: 700;
}
.sub {
    color: #333333;
    font-size: 16px;
}
.small-muted {
    color: #666666;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown("<h1 class='title'>🤖 AI Career Personality Test — BTS Edition</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Discover what AI can do in <em>your</em> role — practical, ROI-focused, and tailored for professionals.</p>", unsafe_allow_html=True)

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

# ---------------------- UTILS ----------------------
def strip_emojis_and_control_chars(text: str) -> str:
    # Remove emojis and control chars to avoid PDF glyph issues
    # Keep basic punctuation, letters, numbers and common unicode.
    # This uses a broad regex to remove emoji-like ranges.
    try:
        # Remove common emoji ranges
        emoji_pattern = re.compile(
            "["
            "\U0001F300-\U0001F6FF"  # symbols & pictographs
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"
            "\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\u200d"  # zero width joiner
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub("", text)
    except Exception:
        # Fallback: remove non-basic characters
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
    # Remove excess blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def make_pdf_from_text(text: str, logo_path: str = None):
    # Create a temp PDF using reportlab Platypus for good wrapping
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=60)
    styles = getSampleStyleSheet()
    normal = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.black,
    )
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1f6feb"),
        spaceAfter=8
    )

    story = []
    # Optionally add logo
    if logo_path and os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=1.6*inch, height=1.6*inch)
            story.append(img)
            story.append(Spacer(1, 8))
        except Exception:
            pass

    # Split into sections by double newline for nicer headings
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    for i, part in enumerate(parts):
        # if part looks like a heading (starts with emoji or '1)' etc), use title style
        if len(part.splitlines()) == 1 and len(part) < 80 and (part.endswith(":") or part.isupper() or part.startswith("🎯") or part[0].isdigit()):
            story.append(Paragraph(part, title_style))
        else:
            story.append(Paragraph(part.replace("\n", "<br/>"), normal))
        story.append(Spacer(1, 8))

    doc.build(story)
    return tmp.name

# ---------------------- BACKEND & UI OUTPUT ----------------------
if submit:
    if not role or not daily_tasks:
        st.warning("Please fill in at least your role and daily tasks.")
    else:
        with st.spinner("Generating your personalized AI profile…"):
            prompt = f"""
You are an expert career strategist + AI productivity mentor. 
Create a premium BTS-style "AI Career Profile" based on:

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
3) 🚀 TOP 3–5 USE CASES (WHAT + IMPACT + FIRST STEP)
4) 💼 BUSINESS IMPACT & QUICK ROI
5) 🧭 6-WEEK ROADMAP (1 line/week)
6) 🛠 TOOL + ONE STARTER PROJECT
7) 👥 TEAM PILOT PLAN (if team_size > 0 or seniority in Manager/Head/Founder)
8) 💬 PROOF LINE
9) 👋 SOFT CTA

Tone: sharp, professional, mobile-friendly, premium, no fluff.
Keep output concise and use bullets where helpful.
Max 450 words.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=750,
                    temperature=0.18
                )
                # New SDK object access pattern
                result = response.choices[0].message.content
            except Exception as e:
                st.error("Error from API — check logs. " + str(e))
                result = None

        if result:
            # Show on page (HTML container). Ensure visible text color by CSS above.
            st.markdown("### 🎉 Your Personalized AI Career Profile")
            # Keep the original text for display, but remove leading/trailing blank lines
            display_text = result.strip()
            st.markdown(f"<div class='report-box'>{display_text.replace(chr(10), '<br/>')}</div>", unsafe_allow_html=True)

            # Prepare PDF (strip emojis for safety)
            pdf_text = strip_emojis_and_control_chars(result)
            # Optional: if you have a logo file in the app folder, set logo_path to its path
            logo_path = None  # e.g., "assets/logo.png"
            pdf_path = make_pdf_from_text(pdf_text, logo_path=logo_path)

            # Offer download
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="📄 Download AI Profile as PDF",
                data=pdf_bytes,
                file_name="AI_Career_Profile.pdf",
                mime="application/pdf"
            )
            st.success("Your AI profile is ready — download and share it.")
