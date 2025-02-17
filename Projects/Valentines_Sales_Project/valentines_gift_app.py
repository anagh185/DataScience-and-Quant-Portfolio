import streamlit as st
import openai
import os
import requests
import re

# 🎨 Streamlit UI Config
st.set_page_config(page_title="CupidAI - Valentine's Gift Finder", page_icon="💝", layout="wide")

# 🔑 Load OpenAI API Key Securely
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API Key is missing! Set it as an environment variable.")
else:
    # Initialize OpenAI Client
    client = openai.OpenAI(api_key=api_key)

# 🎁 Function: AI-Powered Gift Suggestions
def generate_gift_recommendations(budget, recipient, interests):
    """Generate AI-powered Valentine's Day gift recommendations."""
    messages = [
        {"role": "system", "content": "You are an expert Valentine's Day gift advisor."},
        {"role": "user", "content": f"I need a deeply personal Valentine's Day gift idea for someone special. My budget is {budget}. They are my {recipient} (e.g., partner, best friend, parent) and they truly love {interests}. Instead of something generic, I want a gift that feels meaningful, emotional, or tied to a shared memory or experience. It should be something that shows I’ve really put thought into it. Avoid overused gifts like chocolates or basic flowers—give me a unique, heartfelt idea that will make them feel special and appreciated."}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "❌ Invalid API Key. Please check your OpenAI API key."
    except openai.error.OpenAIError as e:
        return f"❌ OpenAI API Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# 🛍️ Function: Extract Keywords for Amazon/Etsy Search
def extract_search_keywords(gift_description):
    """Extracts only the first 3-5 words of the gift name for better search results."""
    gift_keywords = re.sub(r'[^a-zA-Z0-9\s]', '', gift_description)  # Remove special characters
    gift_keywords = ' '.join(gift_keywords.split()[:4])  # Limit to first 4 words
    return gift_keywords

def get_product_links(gift_description):
    """Fetches product search links using extracted keywords."""
    search_query = extract_search_keywords(gift_description)
    amazon_url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    etsy_url = f"https://www.etsy.com/search?q={search_query.replace(' ', '+')}"
    return amazon_url, etsy_url

# 🎉 Fun Header
st.markdown(
    "<h1 style='text-align: center; color: #FF4081;'>💝 CupidAI Valentine's Day Gift Guide 💝</h1>",
    unsafe_allow_html=True
)
st.write("### 🌟 Let CupidAI find the **perfect** Valentine's Day gift for your loved one! 🎁")

# 💰 User Inputs
col1, col2, col3 = st.columns(3)
with col1:
    budget = st.selectbox("💰 Budget:", ["<$50", "$50-$100", "$100+"])
with col2:
    recipient = st.selectbox("💖 Who is this for?", ["Partner", "Friend", "Family", "Self-care"])
with col3:
    interests = st.text_input("🎨 Interests (e.g., Jewelry, Tech, Travel, Fitness):")

# 🔍 Generate AI Gift Recommendations
if st.button("🔮 Find the Perfect Gift!"):
    if not api_key:
        st.error("❌ OpenAI API Key is missing. Set it as an environment variable.")
    elif interests:
        st.markdown("## ✨ AI’s Gift Recommendations ✨")
        with st.spinner("Thinking... 💡"):
            recommendations = generate_gift_recommendations(budget, recipient, interests)
        
        # 🎁 Display AI Suggestions
        gifts = recommendations.split("\n")[:2]  # Get first 2 gift ideas
        for gift in gifts:
            if gift.strip():
                st.subheader(f"🎁 {gift.strip()}")  # Show full AI suggestion

                # 🔗 Generate Product Links
                amazon_link, etsy_link = get_product_links(gift.strip())
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"🛒 [**Find on Amazon**]({amazon_link})", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"🛍️ [**Find on Etsy**]({etsy_link})", unsafe_allow_html=True)
                
                st.write("---")  # Divider line
    else:
        st.warning("⚠️ Please enter some interests to get personalized recommendations! 😊")
