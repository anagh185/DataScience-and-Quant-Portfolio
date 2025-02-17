import streamlit as st
import requests
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Streamlit UI Config
st.set_page_config(page_title="CupidAI - Valentine's Gift Finder", layout="wide")

# Add this at the beginning of your app
if 'HUGGING_FACE_TOKEN' not in st.secrets:
    st.text_input("Enter your Hugging Face token:", key="hf_token", type="password")
    if st.session_state.hf_token:
        os.environ['HUGGING_FACE_TOKEN'] = st.session_state.hf_token
else:
    os.environ['HUGGING_FACE_TOKEN'] = st.secrets['HUGGING_FACE_TOKEN']

# Load model with authentication
@st.cache_resource
def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.3",
            token=os.environ.get('HUGGING_FACE_TOKEN')
        )
        model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.3",
            token=os.environ.get('HUGGING_FACE_TOKEN')
        )
        # Uncomment the next line if you have a GPU and want to use it:
        # model = model.to("cuda")
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

# Only proceed with model loading if authentication is present
if 'HUGGING_FACE_TOKEN' in os.environ:
    tokenizer, model = load_model()
    if tokenizer and model:
        st.success("Local model loaded successfully.")
    else:
        st.error("Failed to load model. Please check your authentication token.")
else:
    st.warning("Please enter your Hugging Face token to proceed.")

# Rest of your code remains the same...