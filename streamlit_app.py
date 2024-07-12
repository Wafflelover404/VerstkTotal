import streamlit as st
import os

# Define paths to the pages
PAGE_PATHS = {
    "Welcome !": "welcome_page.py",
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