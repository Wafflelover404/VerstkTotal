from bs4 import BeautifulSoup

def format_html(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    return soup.prettify()

# Example usage
html_code = """
<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>
"""
formatted_html = format_html(html_code)
print(formatted_html)
