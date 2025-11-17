# app.py
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Career Personality Test (BTS)", page_icon="🤖", layout="centered")
st.title("🤖 AI Career Test — BTS Special")
st.subheader("Discover what AI can do for *your* role — quick, practical, and tailored for professionals.")

# Load client (expects OPENAI_API_KEY in Streamlit secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown("**How it works:** Answer a few quick questions. You'll get a short, actionable profile focused on impact and ROI — perfect for professionals, founders, and students.")

st.markdown("---")
with st.form("career_form"):
    role = st.text_input("Your role / job title (e.g., HR Manager, Product Lead, Student)")
    seniority = st.selectbox("Seniority / Decision power", ["Individual Contributor", "Senior IC", "Manager", "Head / Director", "Founder / CXO", "Student / Early"])
    team_size = st.text_input("Team size you influence (0 if none)", value="0")
    daily_tasks = st.text_area("Top 3 daily tasks (comma separated)")
    kpis = st.text_input("Main KPIs or goals (e.g., reduce time, increase leads, save cost)")
    pain_point = st.text_input("Most repetitive or time-consuming task")
    ai_level = st.selectbox("Familiarity with AI", ["Beginner", "Intermediate", "Advanced"])
    learn_style = st.selectbox("Preferred learning style", ["Practical projects", "Short videos + demos", "Read & implement", "Hands-on workshops"])
    time_per_week = st.selectbox("Time you can commit per week", ["<3 hours", "3-5 hours", "6-8 hours", "8+ hours"])
    submit = st.form_submit_button("Generate my AI profile")

if submit:
    if not role or not daily_tasks:
        st.warning("Please fill at least your role and daily tasks.")
    else:
        with st.spinner("Generating your tailored AI profile…"):
            # Build the prompt with user inputs
            prompt = f"""
You are an expert career strategist + AI productivity consultant who writes crisp, professional output for an audience at a technology summit (students, non-tech professionals, tech professionals, founders, and educators). 

Using the inputs below, create a concise, high-value "AI Career Profile" that reads premium and practical. Keep it clear and mobile-friendly (short paragraphs, bullet lists). End with a soft, persona-appropriate CTA.

Inputs:
Role: {role}
Seniority/DecisionPower: {seniority}
Team Size: {team_size}
Daily Tasks: {daily_tasks}
Key KPIs / Goals: {kpis}
Biggest Pain / Repetitive Task: {pain_point}
AI Familiarity: {ai_level}
Preferred Learning Style: {learn_style}
Availability: {time_per_week}

OUTPUT FORMAT (exact sections, in this order). Use short, actionable bullets. Use persona-aware phrasing.

1) 🎯 ONE-LINER SUMMARY
2) 🎭 YOUR AI PERSONALITY TYPE (choose one)
3) 🚀 TOP 3 HIGH-IMPACT USE CASES (WHAT / IMPACT / FIRST STEP)
4) 💼 BUSINESS IMPACT & QUICK ROI (persona tailored)
5) 🧭 6-WEEK ROADMAP (1 line each week)
6) 🛠 TOOL + ONE STARTER PROJECT (no-code if non-tech)
7) 👥 TEAM PILOT / SCALE (IF decision power or team_size > 0)
8) 💬 SHORT PROOFLINE (1 sentence)
9) 👋 SOFT CTA (persona-specific)

Keep the entire output under 450 words. Use crisp bullets. Avoid long paragraphs. Emphasize practical first steps.
"""
            # Call the Chat Completion API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content": prompt}],
                max_tokens=800,
                temperature=0.2
            )
            result = response.choices[0].message["content"]
        st.markdown("### 🎉 Your BTS AI Profile")
        st.markdown(result)
        st.markdown("---")

        # Persona-specific quick actions / CTAs shown visually
        st.markdown("### Next steps (choose one)")
        cols = st.columns(3)
        if cols[0].button("Get the 6-week plan (DM)"):
            st.success("We'll convert this into a step-by-step 6-week plan. (Use 'Show me the plan' in WhatsApp.)")
        if cols[1].button("Request 1-week team pilot"):
            st.success("We’ll prepare a 1-week pilot template you can run with 1-3 people.")
        if cols[2].button("Save & Email me this"):
            st.info("You can copy the text and email it to yourself — or we can add an email-send flow later.")

st.markdown("---")
st.caption("Designed for Bengaluru Tech Summit — pull-first, ROI-focused, and tailored for professionals. No pressure — just usable insights.")
