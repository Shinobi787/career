import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Career Personality Test", page_icon="🤖", layout="centered")

# --- UI HEADER ---
st.title("🤖 AI Career Personality Test")
st.subheader("Discover what AI can do in *your* career — in 60 seconds.")
st.write("Answer a few quick questions. No pressure. No tech required. Just fun + insights.")

st.markdown("---")

# --- QUESTIONS ---
st.header("📝 Quick Questions")

job_role = st.text_input("1. What do you do? (Student, HR, Marketing, Engineer, Founder, etc.)")
daily_tasks = st.text_area("2. What are 3 tasks you do most often?")
ai_level = st.selectbox("3. How familiar are you with AI?", ["Beginner", "Intermediate", "Advanced"])
goal = st.text_input("4. What’s one goal you want to achieve in your career? (Job, promotion, switch, startup)")
pain_point = st.text_input("5. What's something that takes too much time or feels repetitive?")
learn_style = st.selectbox("6. How do you prefer learning?", ["Practical projects", "Video lessons", "Reading", "Hands-on building"])

submit = st.button("✨ Generate My AI Career Profile")

# --- GPT LOGIC ---
if submit:
    if not job_role or not daily_tasks or not goal:
        st.warning("Please fill at least the first three fields.")
    else:
        with st.spinner("Analyzing your responses…"):
            prompt = f"""
You are an expert career strategist + AI productivity mentor.

Create a personalized "AI Career Personality Test Result" based on this person's answers.

Answers:
Role: {job_role}
Daily Tasks: {daily_tasks}
AI Level: {ai_level}
Career Goal: {goal}
Pain Point: {pain_point}
Learning Style: {learn_style}

OUTPUT FORMAT (very important):

## 🎭 Your AI Personality Type
Give ONE type from these or create a new fitting one:
- The Automator
- The Builder
- The Analyst
- The Creator
- The Strategist
- The Innovator

## 🚀 What AI Can Do in YOUR Career
List 3–5 *specific*, tailored examples.
Make it feel personal and practical.

## 🧠 Your 6-Week AI Roadmap (Simple + Clear)
Week-by-week what they should learn, beginner-friendly.

## 🛠 One AI Tool to Try Today
Recommend ONE relevant tool and why.

## 💡 A Custom AI Project You Can Build
Give one beginner-friendly project idea based on their background.

## 👋 Gentle CTA (Pull, Not Push)
End with:
"If you want, I can convert this into a full 6-week learning plan for you."
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message["content"]

        st.markdown("---")
        st.header("🎉 Your AI Career Profile")
        st.write(result)
        st.markdown("---")
        st.info("Want a custom 6-week AI learning plan? Just say 'Show me the plan'!")

