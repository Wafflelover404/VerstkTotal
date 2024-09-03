# This code is a merge of assistant.py and compare.py, using both 
import streamlit as st
import difflib
import requests
import re

context = False

diff_result = ""
st.header("VerstkEdit Ai test.")
st.subheader("User's code:")
st.text("(unnecessary)")
UserCode = st.text_area("")

css = st.markdown("""
<style>
    .st-da st-db st-dc st-f3 st-gp st-gq st-gr st-gs st-gt st-gu st-hc st-cc st-bb st-he st-gx st-gy st-gz st-h0 st-eu st-h1 st-fi st-h2 st-c3 st-c4 st-c5 st-c6 st-h3 st-h4 st-h5 st-h6 st-c7 st-c8 st-c9 st-ca st-h7 st-h8 st-h9 st-ha {
        width: 100%;
    }

    .st-emotion-cache-15hul6a ef3psqc12 {
        width: 100%;
    }       
</style>
""", unsafe_allow_html=True)

def st_codemirror_diff(left, right, opts, key=None): # This function is used to compare Ai-written code with user's one.
        # Generate a diff using difflib
        diff = difflib.unified_diff(
            left.splitlines(keepends=True),
            right.splitlines(keepends=True),
            fromfile='Left',
            tofile='Right',
        )
        diff_result = ''.join(diff)
        return diff_result

opts = { # Options for difference
    "mode": "python",
    "theme": "default",
}

hf_token = st.session_state.get("hf_token", "") # replace with your HuggingFace API key

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1/v1/chat/completions"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()

def replace_assistant(strin):
  e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
  e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
  return e.strip()

def send(prompt):
    print('generating')
    print(prompt)
    for i in range(0, 10):
        try:
            promptd = [{'role': 'system', 'content':""" You are provided with user's code (Optionally) and his request. Your goal is to change and revise his code based on his request. Respond with code only.
                """}, {'role': 'user', 'content': f'{prompt}'}]
            response = query({
               "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": promptd,
                "max_tokens": 4000,
                'stream': False
            })
            print(response['choices'][0]['message']['content'])
            full_response = response['choices'][0]['message']['content']
            return full_response
            break
        except Exception as e:
            print(e)
            pass
    return "Error"

# Here starts the streamlit interface for Ai assistant
if 'hf_token' not in st.session_state:
    st.session_state.hf_token = ""

btn1, btn2 = st.columns(2)

with btn1:
    with st.expander('Assistant configuration'):
        st.markdown("Configure your <a href=https://huggingface.co/settings/tokens>HuggingFace token</a>.", help="User Access Tokens are the preferred way to authenticate an application or notebook to Hugging Face services. You can manage your access tokens in your settings.", unsafe_allow_html=True)
        input_token = st.text_area("Enter your HuggingFace token 🤗")
        cfg1, cfg2 = st.columns(2)

        with cfg1:
            if st.button("Submit !"):
                st.session_state.hf_token = input_token
                st.write(f"Your current HuggingFace token is: {st.session_state.hf_token}")

        with cfg2:
            context = st.checkbox("Code context", help="Tick the checkbox to let Ai see your code.")

        

with btn2:
    with st.expander("Assistant usage"):
        st.markdown("Ask the assistant any coding-related questions. The assistant has your code as context for your request.")
        request = st.text_area("Input your coding question")
        if st.button("Submit!"):
            print("token: ", st.session_state.hf_token)
            print("query: ", request)
            try:
                if context:
                    request = f"""
                        User's request: {request}

                        User's code: {UserCode}
                    """
                else:
                    request = f"""
                        User's request: {request}
                    """
                response = send(request, st.session_state.hf_token)
                if response != "Error":
                    print("Text writing successfully!", response)
                    st.write(f"Ai response finished !")
                    # Display the difference result between user's code and ai's
                    diff_result = st_codemirror_diff(UserCode, response, opts)
                else:
                    print("An error occurred while communicating with TextAi.")
            except Exception as e:
                print(f"An error occurred: {e}")

if diff_result is not None and diff_result is not "":
    st.subheader("Diff Result")
    st.code(diff_result, language='diff')
    st.header("Page preview")
    st.components.v1.html(response)