import streamlit as st

st.title("Configure everything here")
st.markdown("Don't worry, we respect your privacy 🤫")

st.header("Configure your tokens", help="User Access Tokens are the preferred way to authenticate an application or notebook to Hugging Face services. You can manage your access tokens in your settings.")

st.markdown("Configure your <a href=https://huggingface.co/settings/tokens>HuggingFace token</a>.", unsafe_allow_html=True)
hf = st.text_input("Enter your HuggingFace token 🤗", value=st.session_state.get("hf_token", ""))
if hf:
    st.session_state["hf_token"] = hf

st.markdown("Configure your <a href=https://pixabay.com/api/docs/>Pixabay token</a>.", unsafe_allow_html=True)
px = st.text_input("Enter your Pixabay token 🖼️", value=st.session_state.get("px_token", ""))
if px:
    st.session_state["px_token"] = px

st.header("Code assistant settings")
ctxt = st.checkbox("Code context", help="Tick the checkbox to let AI see your code.", value=st.session_state.get("context", False))
if 'context' not in st.session_state:
    st.session_state["context"] = ctxt
else:
    st.session_state["context"] = ctxt