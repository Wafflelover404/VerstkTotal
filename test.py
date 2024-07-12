import streamlit as st
import assistant

st.set_page_config(layout="centered")

if 'hf_token' not in st.session_state:
    st.session_state.hf_token = ""

css = st.markdown("""
<style>
    .st-c2, .st-c3, .st-c4, .st-c7, .st-c8, .st-c9, .st-ca, .st-cb, .st-cc, .st-cd, .st-cz, .st-at, .st-d0, .st-dl, .st-ch, .st-ci, .st-cj, .st-ck, .st-cl, .st-cm, .st-cn, .st-co, .st-aj, .st-ak, .st-al, .st-am, .st-cp, .st-cq, .st-cr, .st-cs, .st-an, .st-ao, .st-ap, .st-aq, .st-ct, .st-cu, .st-cv, .st-cw {
        width: 100%;
    }

    .st-emotion-cache-15hul6a ef3psqc12 {
        width: 100%;
    }       
</style>
""", unsafe_allow_html=True)

with st.popover("AI assistant menu"):
    btn1, btn2 = st.columns(2)
    
    with btn1:
        with st.expander('Assistant configuration'):
            st.markdown("Configure your HuggingFace token to use AI.", help="User Access Tokens are the preferred way to authenticate an application or notebook to Hugging Face services. You can manage your access tokens in your settings.")
            input_token = st.text_area("Enter your HuggingFace token 🤗")
            if st.button("Submit !"):
                st.session_state.hf_token = input_token
                st.write(f"Your current HuggingFace token is: {st.session_state.hf_token}")
    
    with btn2:
        with st.expander("Assistant usage"):
            st.markdown("Ask the assistant any coding-related questions. The assistant has your code as context for your request.")
            request = st.text_area("Input your coding question")
            if st.button("Submit!"):
                print("token: ", st.session_state.hf_token)
                print("query: ", request)
                try:
                    response = assistant.send(request, st.session_state.hf_token)
                    if response != "Error":
                        print("Text writing successfully!", response)
                        st.write(f"Ai response: {response}")
                    else:
                        print("An error occurred while communicating with TextAi.")
                except Exception as e:
                    print(f"An error occurred: {e}")