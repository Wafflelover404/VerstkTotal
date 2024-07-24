import streamlit as st
import streamlit.components.v1 as components
path_to_html = "./coming_soon.html" 

with open(path_to_html,'r') as f: 
    html_data = f.read()

st.components.v1.html(html_data, height=250)