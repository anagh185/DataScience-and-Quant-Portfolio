import streamlit as st
import os
import openai

# Streamlit App Configuration
st.set_page_config(page_title="AI Valentine's Gift Generator", page_icon="💖")
st.title("💖 CupidAI Valentine's Gift Generator")
st.subheader("Get a thoughtful, personalized gift idea for your special someone!")

# Sidebar API Key Input
with st.sidebar:
    api_provider = st.selectbox("Choose your AI provider", ["OpenAI", "Anthropic", "Cohere", "Other"])
    api_key = st.text_input(f"{api_provider} API Key", value="", type="password")

# User Inputs for Personalization
recipient_name = st.text_input("Your partner's first name (optional)")
relationship_type = st.selectbox(
    "Your relationship type", 
    ["Romantic Partner", "Spouse", "Crush", "Long-Distance Partner", "Other"]
)
time_together = st.selectbox(
    "How long have you been together?", 
    ["Less than a year", "1-3 years", "3-5 years", "5+ years"]
)
memory = st.text_area("Share a special moment or something unique about them (optional)")

if st.button("Generate Gift Idea 💝"):
    if not api_key.strip():
        st.error("Please provide an API key to generate personalized gifts.")
    else:
        try:
            # Generate AI Prompt
            prompt = f"""
            Generate a deeply personal and meaningful Valentine's Day gift idea for a {relationship_type}.
            We've been together for {time_together}. Their name is {recipient_name if recipient_name else 'my partner'}.
            {f'A special memory: {memory}' if memory else ''}
            The gift should feel thoughtful, heartfelt, and unique—something that truly shows I care.
            Keep the idea creative and personal, avoiding generic suggestions like 'a watch' or 'chocolates'.
            """

            # Handle Different API Providers
            if api_provider == "OpenAI":
                client = openai.Client(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": "You are a thoughtful and creative gift-giving assistant."},
                              {"role": "user", "content": prompt}]
                )
                gift_idea = response.choices[0].message.content.strip()

            elif api_provider == "Anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-3",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                gift_idea = response.content[0].text.strip()

            elif api_provider == "Cohere":
                import cohere
                client = cohere.Client(api_key)
                response = client.generate(
                    model="command-r",
                    prompt=prompt,
                    max_tokens=200
                )
                gift_idea = response.generations[0].text.strip()

            else:
                st.warning("Currently, only OpenAI, Anthropic, and Cohere APIs are supported. Please enter a valid API key.")
                gift_idea = None

            if gift_idea:
                st.success(f"🎁 **Gift Idea:** {gift_idea}")

        except Exception as e:
            st.error(f"Error: {e}")
