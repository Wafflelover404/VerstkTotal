import random
import os

def count_folders(directory):
    # Use os.listdir() to get a list of all items in the directory
    folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    # Return the count of folders
    return len(folder_list)

def merge_html_files(header_file_path, body_file_path, output_file_path):
    with open(header_file_path, 'r') as header_file, open(body_file_path, 'r') as body_file:
        header = header_file.read()
        body = body_file.read()

    merged_html = header + body

    with open(output_file_path, 'w') as output_file:
        output_file.write(merged_html)

header_path_number = random.randint(1, count_folders("Header"))
body_path_number = random.randint(1, count_folders("Body"))
print(str(count_folders("Header")) + " ~~ Amount of Headers")
print(str(count_folders("Body")) + " ~~ Amount of Body's")
print(header_path_number , "<~ Header num")
print(body_path_number , "<~ Body num")

header_path = f'./Header/ex{header_path_number}/index.html'
body_path = f'./Body/ex{body_path_number}/index.html'

merge_html_files(header_path, body_path, 'output.html')