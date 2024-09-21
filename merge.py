import random
import os
from bs4 import BeautifulSoup

def format_html(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    return soup.prettify()

def count_folders(directory):
    folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return len(folder_list)

def parse_tag(path, tag):
    with open(path, "r") as path_content:
        content = path_content.read()
        soup = BeautifulSoup(content, 'html.parser')
        tag_content = soup.find(tag)
        
        if tag_content:
            return str(tag_content)
        else:
            print(f"No <{tag}> tag found in {path}")
            return ""

def merge_html_files(header_file_path, body_file_path):
    html_body = parse_tag(header_file_path, "body") + parse_tag(body_file_path, "body")
    print("HTML BODY: ", html_body)
    html_style = parse_tag(header_file_path, "style") + parse_tag(body_file_path, "style")
    print("HTML STYLE: ", html_style)
    print("merging")
    
    html_page = format_html(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {html_style}
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """)
    
    if "None" in html_page:
        print("Error occurred. Element not found")
    
    with open("output.html", "w") as file:
        file.write(html_page)

header_path_number = random.randint(1, count_folders("Header"))
body_path_number = random.randint(1, count_folders("Body"))
print(str(count_folders("Header")) + " ~~ Amount of Headers")
print(str(count_folders("Body")) + " ~~ Amount of Body's")
print(header_path_number , "<~ Header num")
print(body_path_number , "<~ Body num")

header_path = f'./Header/ex{header_path_number}/index.html'
body_path = f'./Body/ex{body_path_number}/index.html'

merge_html_files(header_path, body_path)