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
            print(f"The text '{old_text}' was not found in the file '{path}'")


replace_text("Company-name", "Waffler")
replace_text("Company-description", "Waffles are beloved here")