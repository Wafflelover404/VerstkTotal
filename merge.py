import random
import os
import re

def count_folders(directory):
    folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return len(folder_list)

def parse_tag(path, tag):
    with open(path, "r") as path_content:
        content = path_content.read()
        search_tag = f'<{tag}(.*?)</{tag}>'
        html_code = re.search(search_tag, content, re.DOTALL)
        
        if html_code:
            html_code = html_code.group(1)
            print("found")
        else:
            print("No <style> tag found.")
            print(f"Error in ~> {path}")
            print(f"Unfound tag ~> {tag}")
        return html_code

def merge_html_files(header_file_path, body_file_path):
    html_body = str(parse_tag(header_file_path, "body")) + str(parse_tag(body_file_path, "body"))
    print("HTML BODY: ", html_body)
    html_style = str(parse_tag(header_file_path, "style")) + str(parse_tag(body_file_path, "style"))
    print("HTML STYLE: ", html_style)
    print("merging")
    
    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            {html_style}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    if "None" in html_page:
        print("Error occured. Element not found")
    
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