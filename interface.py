import requests
import re
from bs4 import BeautifulSoup
import random
import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

import text_writer  # For page's text
import get_image_topic  # For image's topic
from search_image import get_image_urls  # Image search function

def replace_text(old_text, new_text):
    path = "output.html"
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()
        if old_text in html_content:
            html_content = html_content.replace(old_text, new_text)
            with open(path, "w", encoding="utf-8") as output_file:
                output_file.write(html_content)
            print(f"Replaced placeholders in '{path}'")
        else:
            print(f"The text '{old_text}' was not found in the file '{path}' - FATAL ERROR")

st.title("VerstkAi")
st.subheader("A simple Website generation engine")

# Initialize session state variables
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'company_description' not in st.session_state:
    st.session_state.company_description = ""
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""

# Create an input field for the company names
company_name = st.text_input("Enter the company name", value=st.session_state.company_name)

# Create an input field for the company description
company_description = st.text_area("Enter the company description", value=st.session_state.company_description)

# Create a button
if st.button('Generate'):
    # When pressed, the field content will be written to the session state variables
    st.session_state.company_name = company_name
    st.session_state.company_description = company_description

    if (company_name and company_description):

        os.system("python3 merge.py")  # Merge HTML files to get started"

        topic = f'{company_name} - {company_description}'

        try:
            response = text_writer.send(topic)
            if response != "Error":
                print("Text writing successfully!", response)

                # Emplace company text and name
                replace_text("&Company-name&", company_name)
                replace_text("&Company-description&", response)

            else:
                print("An error occurred while communicating with TextAi.")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            response = get_image_topic.send(topic)
            if response != "Error":
                imgurl_horizontal = random.choice(get_image_urls(response, "horizontal"))
                imgurl_vertical = random.choice(get_image_urls(response, "vertical"))
                replace_text("&Vertical-image&", imgurl_vertical)
                replace_text("&Horizontal-image&", imgurl_horizontal)
                print("Vertical image URL:", imgurl_vertical)
                print("Horizontal image URL:", imgurl_horizontal)
            else:
                print("An error occurred while communicating with TextAi.")
        except Exception as e:
            print(f"An error occurred: {e}")

        print("All processes have completed successfully, and all changes have been written to the HTML code.")

        # Open and read the HTML file
        with open('output.html', 'r') as f:
            html_string = f.read()
            st.session_state.generated_html = html_string

        # Display the HTML file
        components.html(html_string, height=900)

        # Create a button for exporting the HTML file
        # Check if the file exists
        if os.path.exists("output.html"):
            # Read the file
            with open("output.html", "r") as file:
                file_content = file.read()

            # Create a button for downloading the file
            st.download_button(
                label="Export",
                data=file_content,
                file_name="output.html",
                mime="text/html",
            )
        else:
            st.write("The file output.html does not exist in the current directory.")

    else:
        # Open error, cause input's empty
        with open('error.html', 'r') as f:
            html_string = f.read()

        # Display the HTML file
        components.html(html_string, height=900)

# Display the generated HTML if it exists in session state
if st.session_state.generated_html:
    components.html(st.session_state.generated_html, height=900)