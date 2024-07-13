import requests
import random
import streamlit as st

def get_image_urls(query, orientation):
    API_KEY = st.session_state.get("px_token", "")  # replace with your Pixabay API key
    print(API_KEY)
    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo&orientation={orientation}"
    response = requests.get(url)
    data = response.json()
    urls = [img["webformatURL"] for img in data["hits"]]
    return urls


