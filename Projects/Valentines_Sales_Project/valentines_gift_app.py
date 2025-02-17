import streamlit as st
import requests
import os
import re

# Streamlit UI Config
st.set_page_config(page_title="CupidAI - Valentine's Gift Finder", layout="wide")

# Load Hugging Face API Key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    st.error("Hugging Face API Key is missing! Set it as an environment variable.")
else:
    st.success("Hugging Face API Key loaded successfully!")

# AI-Powered Gift Suggestions (Using Hugging Face API)
def generate_gift_recommendations(budget, recipient, interests):
    """Generate AI-powered Valentine's Day gift recommendations using Hugging Face."""
    
    # Recommended model: Mistral 7B (Better at structured output)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    prompt = f"""
    I need three unique, thoughtful Valentine's Day gift ideas for someone special. 
    - Budget: {budget} 
    - Relationship: {recipient} 
    - Interests: {interests} 

    Strictly follow this format:
    1. [Gift Name]: [Short description]  
    2. [Gift Name]: [Short description]  
    3. [Gift Name]: [Short description]  

    Do not include explanations, introductions, or extra text. Only return the list.
    """

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    response_json = response.json()
    if response.status_code == 200 and isinstance(response_json, list) and "generated_text" in response_json[0]:
        return response_json[0]["generated_text"]
    else:
        # Failsafe backup gift suggestions
        return (
            "1. Personalized Star Map: A custom map of the stars from a meaningful date.\n"
            "2. Custom Soundwave Art: A printed soundwave of a special song or voice note.\n"
            "3. Handwritten Letter Necklace: A pendant with an engraved handwritten message."
        )

# Extract Keywords for Amazon/Etsy Search
def extract_search_keywords(gift_description):
    """Extracts only the first 3-5 words of the gift name for better search results."""
    gift_keywords = re.sub(r'[^a-zA-Z0-9\s]', '', gift_description)  # Remove special characters
    gift_keywords = gift_keywords.split(":")[0]  # Extract only the gift name before ':'
    gift_keywords = ' '.join(gift_keywords.split()[:4])  # Limit to first 4 words
    return gift_keywords.strip()

def get_product_links(gift_description):
    """Fetches product search links using extracted keywords."""
    search_query = extract_search_keywords(gift_description)
    amazon_url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    etsy_url = f"https://www.etsy.com/search?q={search_query.replace(' ', '+')}"
    return amazon_url, etsy_url

# Fun Header
st.markdown(
    "<h1 style='text-align: center; color: #FF4081;'>CupidAI - Valentine's Day Gift Guide</h1>",
    unsafe_allow_html=True
)
st.write("Let CupidAI find the perfect Valentine's Day gift for your loved one!")

# User Inputs
col1, col2, col3 = st.columns(3)
with col1:
    budget = st.selectbox("Budget:", ["<$50", "$50-$100", "$100+"])
with col2:
    recipient = st.selectbox("Who is this for?", ["Partner", "Friend", "Family", "Self-care"])
with col3:
    interests = st.text_input("Interests (e.g., Jewelry, Tech, Travel, Fitness):")

# Generate AI Gift Recommendations
if st.button("Find the Perfect Gift!"):
    if not HUGGINGFACE_API_KEY:
        st.error("Hugging Face API Key is missing. Set it as an environment variable.")
    elif interests:
        st.markdown("### AI’s Gift Recommendations")
        with st.spinner("Thinking..."):
            recommendations = generate_gift_recommendations(budget, recipient, interests)
        
        # Extract AI Suggestions using regex for better accuracy
        gift_suggestions = re.findall(r"\d+\.\s(.+?):\s(.+)", recommendations)

        if not gift_suggestions:
            st.error("AI response was invalid. Showing default gift suggestions.")
            gift_suggestions = [
                ("Personalized Star Map", "A custom map of the stars from a meaningful date."),
                ("Custom Soundwave Art", "A printed soundwave of a special song or voice note."),
                ("Handwritten Letter Necklace", "A pendant with an engraved handwritten message."),
            ]

        # Display AI Suggestions
        for gift_name, gift_desc in gift_suggestions[:3]:  # Ensure max 3 suggestions
            st.subheader(f"{gift_name}")
            st.write(gift_desc)

            # Generate Product Links
            amazon_link, etsy_link = get_product_links(gift_name)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[Find on Amazon]({amazon_link})", unsafe_allow_html=True)
            with col2:
                st.markdown(f"[Find on Etsy]({etsy_link})", unsafe_allow_html=True)
            
            st.write("---")  # Divider line
