import streamlit as st
st.set_page_config(layout="wide")

# Initialize session state with default values if they don't exist
if 'hf_token' not in st.session_state:
    st.session_state.hf_token = ""
if 'px_token' not in st.session_state:
    st.session_state.px_token = ""
if 'context' not in st.session_state:
    st.session_state.context = False

# Define paths to the pages
PAGE_PATHS = {
    "Welcome !": "welcome_page.py",
    "Configure": "config.py",
    "Create your page": "interface.py",
    "Redact your page": "editor.py"
}

def load_page(path):
    with open(path, 'r') as file:
        page_code = file.read()
    exec(page_code, globals())

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Pages: ", list(PAGE_PATHS.keys()))

    # Load and display the selected page
    page_path = PAGE_PATHS[selection]
    load_page(page_path)

if __name__ == "__main__":
    main()