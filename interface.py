# Page generation

import requests
import re
from bs4 import BeautifulSoup
import random
import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess
import sqlite3

import text_writer  # For page's text
import get_image_topic  # For image's topic
from search_image import get_image_urls  # Image search function

# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = ""
if 'edited_content' not in st.session_state:
    st.session_state.edited_content = ""

ready = False

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
if st.session_state["hf_token"] == "" or st.session_state["px_token"] == "":
    st.warning("Make sure to configure your keys")

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

    if st.session_state["hf_token"] == "" or st.session_state["px_token"] == "":
        st.error("Configure you acces keys at 'configure' page")
    else:
        ready = False
        # When pressed, the field content will be written to the session state variables
        st.session_state.company_name = company_name
        st.session_state.company_description = company_description

        open("output.html", 'w').close()

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
            ready = True

if ready:
    # Open and read the HTML file
    with open('output.html', 'r') as f:
        html_string = f.read()
        st.session_state.generated_html = html_string
        components.html(st.session_state.generated_html, height=900)

    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        with st.popover("Export"):
            filename = st.text_input(label="Enter filename", key='filename2')
            if st.download_button(
                label="Export",
                data=st.session_state.edited_content,
                file_name=filename,
                key=f"Download"
            ):
                st.success("Download started!")

    with btn2:
        with st.popover("Save to account"):
            if st.session_state.account:
                filename = st.text_input(label="Enter filename", key='filename1')
                if st.button(label="Submit"):
                    with sqlite3.connect(st.session_state.db_path) as db:
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, st.session_state.generated_html))
                        file_id = cursor.lastrowid
                        cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (st.session_state.account_id, file_id))
                        db.commit()
                    st.success(f"File added to the database with file_id: {file_id}")
                    st.success("Saved to your account. Visit the login page to see.")
            else:
                st.error("Login to save your files.")

    with btn3:
        if st.button(label="Edit", help="Open this file in code editor"):
            st.session_state.edited_content = st.session_state.generated_html
            st.success("Opened in Web Editor!")
