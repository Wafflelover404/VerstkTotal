import streamlit as st


st.title("Welcome to *Constructify* ! :wave:")
st.subheader("A simple website editor with cool functions of generating web-pages powered by AI algorithms")
st.header("Developers:")
st.write("(our github profiles)")
with st.container():
    gen, edit, space = st.columns([1, 1, 3])
    gen.link_button("Afanasyeff Ivan :black_cat:", "https://github.com/wafflelover404")
    edit.link_button("Vinogradov Timofey :black_cat:", "https://github.com/DolphyXSTD")
st.markdown("This project is built with <a href='https://streamlit.io/'>Streamlit :crown:</a> and <a href='https://huggingface.co/'>HuggingFace :hugging_face:</a>.", unsafe_allow_html=True)
st.subheader("Check out the repositories:")
with st.container():
    gen, edit, space = st.columns([1, 1, 3])
    gen.link_button("VerstkaGen repository", "https://github.com/Wafflelover404/VerstkaGen")
    edit.link_button("VerstkEdit repository", "https://github.com/Wafflelover404/VerstkEdit")
st.subheader("Contact us:")
st.link_button("Contact us !", "https://google.com")
