import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant", page_icon="✍️", layout="centered"
)

# App header
st.title("✍️ AI Content Assistant")
st.markdown(
    "Generate engaging posts, captions, and hashtags tailored for your target"
    " audience."
)

# API Key Configuration
# You can use st.secrets for Streamlit Cloud deployment or input it in the sidebar
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input(
    "Enter Groq API Key", type="password", help="Get a free key from console.groq.com"
)

# Fallback to environment variables if available
api_key = api_key_input or os.environ.get("GROQ_API_KEY")

# Input Form
with st.form("content_form"):
  col1, col2 = st.columns(2)

  with col1:
    content_type = st.selectbox(
        "Content Type",
        [
            "Social Media Post",
            "Blog Intro",
            "Product Announcement",
            "Educational Tip",
            "Motivational Quote",
        ],
    )
    platform = st.selectbox(
        "Platform", ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "TikTok"]
    )
    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Casual & Friendly",
            "Humorous",
            "Persuasive",
            "Inspirational",
        ],
    )

  with col2:
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Tech Founders, Students, Fitness Beginners",
    )
    topic = st.text_area(
        "Topic / Key Message",
        placeholder="e.g., Why learning Python is essential in 2026...",
        height=106,
    )

  submitted = st.form_submit_button("Generate Content 🚀")

# Generation Logic
if submitted:
  if not api_key:
    st.error(
        "⚠️ Please enter your Groq API Key in the sidebar or set it in your"
        " environment secrets."
    )
  elif not topic.strip():
    st.warning("⚠️ Please enter a topic or key message.")
  else:
    try:
      client = Groq(api_key=api_key)

      prompt = f"""
            You are an expert copywriter and social media manager.
            Create a complete, high-performing post based on the following parameters:
            - Content Type: {content_type}
            - Platform: {platform}
            - Tone: {tone}
            - Target Audience: {target_audience}
            - Topic/Key Message: {topic}

            Format your response clearly with:
            1. An attention-grabbing hook/headline.
            2. The main post body/caption.
            3. A list of relevant, high-reaching hashtags at the bottom.
            """

      with st.spinner("Generating your content..."):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",  # Free, fast Groq model
            temperature=0.7,
        )

        result = chat_completion.choices[0].message.content

      st.success("✨ Content Generated Successfully!")
      st.markdown("### Generated Output")
      st.markdown(result)

      # Download button for the generated content
      st.download_button(
          label="Download Content as Text File",
          data=result,
          file_name="ai_generated_content.txt",
          mime="text/plain",
      )

    except Exception as e:
      st.error(f"An error occurred: {e}")
