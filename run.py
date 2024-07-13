import requests
import re
from bs4 import BeautifulSoup
import os
import random

hf_token = input("Token ~>")

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

os.system("python3 merge.py")  # Merge HTML files to get started"

company_name_inp = input("Company name ~> ")
company_desc_inp = input("Company Description ~> ")

print("Token: ", hf_token)
print("Name: ", company_name_inp)
print("Desc:", company_desc_inp)
topic = f'{company_name_inp} - {company_desc_inp}'

try:
    response = text_writer.send(topic, hf_token)
    if response != "Error":
        print("Text writing successfully!", response)

        # Emplace company text and name
        replace_text("&Company-name&", company_name_inp)
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
