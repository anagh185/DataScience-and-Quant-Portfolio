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

# AI-Powered Gift Suggestions (Using Hugging Face LLaMA 3)
def generate_gift_recommendations(budget, recipient, interests):
    """Generate AI-powered Valentine's Day gift recommendations using LLaMA 3."""
    
    API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    prompt = f"""
    I need three unique, thoughtful Valentine's Day gift ideas for someone special. 
    - Budget: {budget} 
    - Relationship: {recipient} 
    - Interests: {interests} 

    Instead of something generic, I want gifts that feel meaningful, emotional, or tied to a shared memory.
    Each suggestion should be numbered (1, 2, 3) and formatted exactly like this:

    1. Gift Name: Short description  
    2. Gift Name: Short description  
    3. Gift Name: Short description  

    No introductory text, no explanations—just three gift ideas in this exact format.
    Avoid overused ideas like chocolates or basic flowers.
    """

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        return response.json()[0]["generated_text"]  # Extract AI response
    else:
        return "AI model unavailable. Try again later."

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
        
        # Display AI Suggestions
        gift_suggestions = recommendations.split("\n")[:3]  # Get first 3 gift ideas
        for gift in gift_suggestions:
            if gift.strip():
                st.subheader(f"{gift.strip()}")  # Show full AI suggestion

                # Generate Product Links
                amazon_link, etsy_link = get_product_links(gift.strip())
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"[Find on Amazon]({amazon_link})", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"[Find on Etsy]({etsy_link})", unsafe_allow_html=True)
                
                st.write("---")  # Divider line
