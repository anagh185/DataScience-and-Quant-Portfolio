
import streamlit as st
import requests
import time
import urllib.parse  # For formatting Amazon search links
import random  # To randomize extra Amazon gift suggestions
import os
 # Replace with your API key
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
# ---- STREAMLIT PAGE CONFIG ----
st.set_page_config(
    page_title="CupidAI - Gift Generator",
    page_icon="💖",
    layout="centered"
)

# ---- STYLING ----
st.markdown("""
    <style>
        .stButton>button {
            background-color: #FF4B4B !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div>select {
            font-size: 16px !important;
        }
        .stTextArea>div>textarea {
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💖 CupidAI: Personalized Gift Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Find the perfect heartfelt gift for your special someone! 🎁</p>", unsafe_allow_html=True)

# ---- USER INPUTS ----
with st.form("gift_form"):
    st.markdown("### 🎀 Personalize Your Gift")
    recipient_name = st.text_input("Partner's Name (Optional)", placeholder="e.g., Alex")
    relationship_type = st.selectbox("Relationship Type", ["Romantic Partner", "Spouse", "Crush", "Long-Distance Partner", "Other"])
    time_together = st.selectbox("Time Together", ["Less than a year", "1-3 years", "3-5 years", "5+ years"])
    memory = st.text_area("✨ Share a Special Moment (Optional)", placeholder="E.g., We once danced in the rain and laughed endlessly.")

    submit = st.form_submit_button("💝 Generate Gift Idea")

# ---- AI REQUEST ----
if submit:
    with st.spinner("✨ Generating the perfect gift idea..."):
        time.sleep(1.5)  # Simulated delay for better UX
        
        
        
        # Define the AI prompt
        prompt = f"""
        You are a creative and romantic AI helping users find the perfect Valentine's Day gift.
        Please generate a heartfelt, unique, and personal gift idea in this format, with each on a new line and it should be as AI is suggesting gifts:

        💌 **[Random poetic line, short and romantic]**  
        \n🎁 **Gift Idea:** [Describe the personalized gift]  
        \n💖 **Why it’s special:** [Explain why it’s meaningful and how it will make them feel]  
        \n💕 **A final romantic touch:** [End with a short, poetic line or romantic sentiment]

        Also, suggest 2 related gifts that match the theme of the personalized gift. These should be thoughtful and complement the main gift.
        
        **Details for the gift suggestion:**
        - Relationship: {relationship_type}
        - Time together: {time_together}
        - Name: {recipient_name if recipient_name else 'my partner'}
        {f'- A special memory: {memory}' if memory else ''}

        Avoid generic gifts like "a watch" or "flowers." The gift should feel **thoughtful, romantic, and deeply personal**.
        Make sure the response feels **warm, affectionate, and poetic.**
        """

        # Mistral API request
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-tiny",
            "messages": [
                {"role": "system", "content": "You are a thoughtful and creative gift-giving assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300
        }

        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()

        if "choices" in response_json:
            gift_idea = response_json["choices"][0]["message"]["content"].strip()

            # ---- EXTRACT MAIN IDEA FOR AMAZON SEARCH ----
            gift_lines = gift_idea.split("\n")
            main_gift = gift_lines[1].replace("🎁 **Gift Idea:**", "").strip()  # Extract main gift idea
            amazon_keywords = " ".join(main_gift.split()[:3])  # Use first 2-3 words as keywords

            # Randomized alternative gift ideas
            extra_gifts = [
                "Custom Love Letter Keepsake",
                "Personalized Soundwave Art of 'I Love You'",
                "Engraved Coordinates Bracelet",
                "Handwritten Love Book",
                "Couple's Star Map Canvas",
                "Date Night Adventure Book",
                "Handmade Love Coupons",
                "Couple's Memory Jar",
                "Customized Spotify Code Plaque",
                "Personalized Love Story Comic Book",
                "Message in a Bottle Love Notes",
                "Romantic Scavenger Hunt Kit",
                "A Box of Open-When Letters",
                "Custom Song Written About Your Love",
                "3D Moon Lamp with Engraved Love Note"
            ]
            alt_gift1, alt_gift2 = random.sample(extra_gifts, 2)

            # Amazon Search Links
            amazon_alt1_link = f"https://www.amazon.com/s?k={urllib.parse.quote(alt_gift1)}"
            amazon_alt2_link = f"https://www.amazon.com/s?k={urllib.parse.quote(alt_gift2)}"

            # ---- DISPLAY GIFT IDEA ----
            st.success("🎁 **Your Personalized Gift Idea:**")
            st.markdown(f"""
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    box-shadow: 2px 2px 15px rgba(255, 75, 75, 0.2);
                    font-size: 18px;">
                    {gift_idea}
                </div>
            """, unsafe_allow_html=True)

            # ---- AMAZON LINKS ----
            st.markdown(f"""
                🛍️ **Shop on Amazon:**
                \n🔗 **Optional Gift 1:** [{alt_gift1}]({amazon_alt1_link})  
                \n🔗 **Optional Gift 2:** [{alt_gift2}]({amazon_alt2_link})  
            """, unsafe_allow_html=True)

        else:
            st.error("⚠️ Unable to generate a response. Please check your API key or try again later.")

# ---- FOOTER ----
st.markdown("""
    <hr>
    <p style="text-align: center;">Made with ❤️ by CupidAI</p>
""", unsafe_allow_html=True)
