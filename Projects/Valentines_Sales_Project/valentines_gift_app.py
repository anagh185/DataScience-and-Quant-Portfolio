import openai
import streamlit as st
import os
# Streamlit App
st.set_page_config(page_title="AI Valentine's Gift Generator", page_icon="💖")
st.title("💖 CupidAI Valentine's Gift Generator")
st.subheader("Get a thoughtful, personalized gift idea for your special someone!")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# User Inputs
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", value="", type="password")

recipient_name = st.text_input("Your partner's first name (optional)")
relationship_type = st.selectbox("Your relationship type", ["Romantic Partner", "Spouse", "Crush", "Long-Distance Partner", "Other"])
time_together = st.selectbox("How long have you been together?", ["Less than a year", "1-3 years", "3-5 years", "5+ years"])

# Optional deeper personalization without overwhelming the user
memory = st.text_area("Share a special moment or something unique about them (optional)")

if st.button("Generate Gift Idea 💝"):
    if not openai_api_key.strip():
        st.error("Please provide an OpenAI API key to generate personalized gifts.")
    else:
        try:
            client = openai.Client(api_key=openai_api_key)
            
            # AI Prompt
            prompt = f"""
            Generate a deeply personal and meaningful Valentine's Day gift idea for a {relationship_type}.
            We've been together for {time_together}. Their name is {recipient_name if recipient_name else 'my partner'}.
            {f'A special memory: {memory}' if memory else ''}
            The gift should feel thoughtful, heartfelt, and unique—something that truly shows I care.
            Keep the idea creative and personal, avoiding generic suggestions like 'a watch' or 'chocolates'.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a thoughtful and creative gift-giving assistant."},
                          {"role": "user", "content": prompt}]
            )
            
            gift_idea = response.choices[0].message.content.strip()
            st.success(f"🎁 **Gift Idea:** {gift_idea}")
        except Exception as e:
            st.error(f"Error: {e}")
