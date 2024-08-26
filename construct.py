import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import requests
from io import BytesIO
from requests.exceptions import RequestException

st.markdown("""
<style>
.main > div {
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

# page initialization
if 'input_page' not in st.session_state:
    st.session_state.input_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<style>
</style>
</head>
<body>
</body>
</html>"""


# gets ready components
def fetch_components():
    try:
        response = requests.get('http://127.0.0.1:8000/api/components/')
        response.raise_for_status()
        st.session_state.not_working = False
        return response.json()
    except RequestException:
        st.session_state.not_working = True
        return []


# gets original image resolution
def get_image_dimensions(url):
    if url != '':
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        st.session_state.form_data[1]['orig-w'] = img.width
        st.session_state.form_data[1]['orig-h'] = img.height


# checks url on valid
def is_image_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except RequestException:
        return False


# finds parameters of class for form filling in editing mode
def get_class_params(page, edited_class, type):
    html, css = find_html_and_css(page, edited_class)
    if type == 'text':
        color = css[css.find("color"):]
        color = color[color.find("#"):color.find("#") + 7]

        if css.find("font-size") > 0:
            size = css[css.find("font-size"):]
            size = int(size[size.find(":") + 2: size.find('px')])
        else:
            size = 16

        align = css[css.find("text-align"):]
        align = align[align.find(":") + 2: align.find(';')]
        align_index = 0
        if align == 'center':
            align_index = 1
        elif align == 'right':
            align_index = 2

        inc = 3
        bold = False
        if html.find("<b>") + html.find("</b>") > 0:
            bold = True
            inc += 3
        italic = False
        if html.find("<i>") + html.find("</i>") > 0:
            italic = True
            inc += 3
        under = False
        if html.find("<u>") + html.find("</u>") > 0:
            under = True
            inc += 3

        text = html[html.find("<p>") + inc: html.find("</p>") - (inc + inc // 3 - 1) + 3]
        st.session_state.form_data[0] = {
            'text': text,
            'color': color,
            'isBold': bold,
            'isItalic': italic,
            'isUnder': under,
            'size': size,
            'align': align,
            'align-index': align_index
        }
    elif type == 'image':
        html = html[html.find("config"):]
        url = html[html.find("config") + 4:html.find('>')]
        get_image_dimensions(url)
        orig_w = st.session_state.form_data[1]['orig_w']
        orig_h = st.session_state.form_data[1]['orig_h']

        html2, css2 = find_html_and_css(page, edited_class + ' img')
        keep = False
        native = False
        if css2.find('px') > 0:
            res_w = int(css2[css2.find("width:") + 6:css2.find("px")])
            css2 = css2[css2.find("px") + 3:]
            res_h = int(css2[css2.find("height:") + 7:css2.find("px")])
            rt = "px"
            rt_index = 0
            res_wp = round(orig_w / res_w * 100)
            res_hp = round(orig_h / res_h * 100)
        elif css2.find('%') > 0:
            res_wp = int(css2[css2.find("width:") + 6:css2.find("%")])
            if css.find('padding') > 0:
                width_str = css[css.find('width:'):]
                frame_res_wp = int(width_str[width_str.find("width:") + 6:width_str.find("%")])
                res_wp = round(100 / frame_res_wp * res_wp)
            css2 = css2[css2.find("%") + 2:]
            print(css2)
            res_hp = int(css2[css2.find("height:") + 7:css2.find("%")])
            rt = "%"
            rt_index = 1
            res_w = round(orig_w * res_wp / 100)
            res_h = round(orig_h * res_hp / 100)
        else:
            native = True
            res_w = orig_w
            res_h = orig_h
            res_wp = 100
            res_hp = 100
            rt = 'px'
            keep = True
            rt_index = 0

        align = css[css.find("text-align"):]
        align = align[align.find(":") + 2: align.find(';')]
        align_index = 0
        if align == 'center':
            align_index = 1
        elif align == 'right':
            align_index = 2

        st.session_state.form_data[1] = {
            'url': url,
            'native': native,
            'rt': rt,
            'rt-index': rt_index,
            'keep_props': keep,
            'orig_w': orig_w,
            'orig_h': orig_h,
            'res-w': res_w,
            'res-h': res_h,
            'res-wp': res_wp,
            'res-hp': res_hp,
            'align': align,
            'align-index': align_index
        }
    if css.find("padding") > 0:
        padding_str = css[css.find("padding:"):]
        pad = int(padding_str[padding_str.find('padding:') + 9:padding_str.find('px')])

        width_str = css[css.find("width:"):]
        width_str = width_str[:width_str.find(';')]
        if width_str.find('px') > 0:
            width_val = int(width_str[width_str.find('width:') + 7:width_str.find('px')])
        else:
            width_val = int(width_str[width_str.find('width:') + 7:width_str.find('%')])
        if css.find('margin-left') > 0 and css.find('margin-right') > 0:
            margin = 'fcenter'
            margin_index = 1
        elif css.find('margin-left') > 0:
            margin = 'fright'
            margin_index = 2
        else:
            margin = 'fleft'
            margin_index = 0

        if css.find("background-color") > 0:
            back = css[css.find("background-color") + 18:css.find("background-color") + 25]
            noBg = False
        else:
            noBg = True
            back = '#ffffff'
        if css.find("border") > 0:
            isBorder = True
            border = css[css.find("border:"):]
            thick = int(border[border.find("border:") + 8: border.find('px')])
            color = border[border.find('#'):border.find('#') + 7]
            round_str = css[css.find("border-radius"):]
            radius = int(round_str[round_str.find("radius:") + 8: round_str.find("px")])
        else:
            isBorder = False
            thick = 2
            color = '#000000'
            radius = 10
        st.session_state.form_data[2] = {
            'frame': True,
            'width': width_val,
            'align': margin,
            'align-index': margin_index,
            'padding': pad,
            'noBg': noBg,
            'bg': back,
            'border': isBorder,
            'thick': thick,
            'round': radius,
            'borderColor': color
        }
    else:
        st.session_state.form_data[2] = {
            'frame': False,
            'width': 100,
            'align': 'fleft',
            'align-index': 0,
            'padding': 20,
            'noBg': True,
            'bg': '#ffffff',
            'border': True,
            'thick': 2,
            'round': 10,
            'borderColor': '#000000'
        }


# finds html and css of class to edit or delete it
def find_html_and_css(page, obj):
    class_css = page.find(f".{obj}")
    raw_page = page[class_css:]
    scope_index = raw_page.find("}") + class_css
    css = page[class_css:scope_index + 2]

    html_start = 0
    html_end = 0
    raw_page = page
    new_class = ""
    if obj.endswith("img"):
        html = None
    else:
        while new_class != obj:

            html_start = raw_page.find("<div")
            html_end = raw_page.find("</div>") + 5
            end = raw_page.find(">")
            new_class = raw_page[html_start:end]
            new_class = new_class[new_class.find("=") + 1:]
            new_class = new_class.replace(" ", "")
            if new_class == obj:
                break
            raw_page = raw_page[end + 1:]
            start = raw_page.find("class")
            end = raw_page.find(">")
            while end < start:
                raw_page = raw_page[end + 1:]
                start = raw_page.find("class")
                end = raw_page.find(">")
        html = raw_page[html_start - 1:html_end + 2]

    return html, css


def find_classes(page):  # rewrite
    body = page.find("<body>") + 6
    page = page[body:]
    found_classes = []
    # finding classes
    while page.find("class") > -1:

        start = page.find("class")
        end = page.find(">")
        new_class = page[start:end]
        new_class = new_class[new_class.find("=") + 1:]
        new_class = new_class.replace(" ", "")
        if new_class not in found_classes:
            found_classes.append(new_class)

        page = page[end + 1:]
        start = page.find("class")
        end = page.find(">")
        while end < start:
            page = page[end + 1:]
            start = page.find("class")
            end = page.find(">")

    return found_classes


classes = find_classes(st.session_state.input_page)


# creates text element with form parameters
def create_text(text, color, bold, italic, under, size, align):
    css_string = f"\tcolor: {color};\n\ttext-align: {align};\n"

    if text_size != 16:
        css_string += f"\tfont-size: {size}px;\n"

    string = f"<p>{text}</p>"
    if bold:
        string = string.replace("<p>", "<p><b>")
        string = string.replace("</p>", "</b></p>")
    if italic:
        string = string.replace("<p>", "<p><i>")
        string = string.replace("</p>", "</i></p>")
    if under:
        string = string.replace("<p>", "<p><u>")
        string = string.replace("</p>", "</u></p>")
    if isFrame:
        css_string = add_frame('text', css_string)
    return string, css_string


# creates image element with form parameters
def create_image(url, rt, res_w, res_h, align):
    css_string = f"\ttext-align: {align};\n"
    string = f'<img config={url}>'
    css_image = ''
    if not isNative:
        if isFrame and rt == '%':
            css_image = f"\twidth: {round(100 / width * res_w)}%;\n\theight: {res_h}%;\n"
        else:
            css_image = f"\twidth: {res_w}{rt};\n\theight: {res_h}{rt};\n"
    if isFrame:
        css_string = add_frame('image', css_string)
    return string, css_string, css_image


# adds frame to element if needed
def add_frame(type, css):
    css += f"\tpadding: {padding}px;\n"
    if type == 'text':
        css += f"\twidth: {width}%;\n"
    elif type == 'image':
        if resolution_type == 'px':
            css += f"\twidth: {width}px;\n"
        elif resolution_type == '%':
            css += f"\twidth: {width}%;\n"
    if frame_alignment == 'left':
        css += "\tmargin-right: auto;\n"
    elif frame_alignment == 'right':
        css += "\tmargin-left: auto;\n"
    else:
        css += "\tmargin-left: auto;\n"
        css += "\tmargin-right: auto;\n"
    if not isNoBg:
        css += f"\tbackground-color: {background};\n"
    if hasBorder:
        css += f"\tborder: {thickness}px solid {borderColor};\n"
        css += f"\tborder-radius: {rounding}px;\n"
    return css


# adds new class with given type
def add_class(page, type):
    global classes

    new_class = 0
    if type == 'text':
        if text_to_add == '':
            return
        new_class = 'p0'
        for i in range(len(classes) - 1, -1, -1):
            if classes[i].startswith("p"):
                new_class = 'p' + str(int(classes[i][1:]) + 1)
                break

        new_html, new_css = create_text(text_to_add, color_text, isBold, isItalic, isUnder, text_size, alignment)

    elif type == 'image':
        if image_url == '':
            return
        if resolution_type == 'px':
            res_w = st.session_state.form_data[1]['res-w']
            res_h = st.session_state.form_data[1]['res-h']
        else:
            res_w = st.session_state.form_data[1]['res-wp']
            res_h = st.session_state.form_data[1]['res-hp']
        new_class = 'i0'
        for i in range(len(classes) - 1, -1, -1):
            if classes[i].startswith("i"):
                new_class = 'i' + str(int(classes[i][1:]) + 1)
                break
        new_html, new_css, image_css = create_image(image_url, resolution_type, res_w, res_h, alignment)

    new_css = f".{new_class}" + "{\n" + new_css + "}\n</style>"
    new_html = f"\t<div class={new_class}>\n\t\t{new_html}\n\t</div>\n</body>"
    page = page.replace("</style>", new_css)
    page = page.replace("</body>", new_html)
    if type == 'image':
        image_css = f".{new_class} img" + "{\n" + image_css + "}\n</style>"
        page = page.replace("</style>", image_css)

    classes.append(new_class)
    return page


# edit class by replacing old html with new one
def edit_class(page, type, edited_class):
    html, css = find_html_and_css(page, edited_class)

    if type == 'text':
        if text_to_add == '':
            return
        new_html, new_css = create_text(text_to_add, color_text, isBold, isItalic, isUnder, text_size, alignment)

    elif type == 'image':
        if image_url == '':
            return
        if resolution_type == 'px':
            res_w = st.session_state.form_data[1]['res-w']
            res_h = st.session_state.form_data[1]['res-h']
        else:
            res_w = st.session_state.form_data[1]['res-wp']
            res_h = st.session_state.form_data[1]['res-hp']
        new_html, new_css, image_css = create_image(image_url, resolution_type, res_w, res_h, alignment)

    new_css = f".{edited_class}" + "{\n" + new_css + "}\n</style>"
    new_html = f"\t<div class={edited_class}>\n\t\t{new_html}\n\t</div>\n</body>"
    page = page.replace(html, new_html)
    if image_css is not None:
        image_css = f".{edited_class} img" + "{\n" + image_css + "}\n</style>"
        new_css += image_css
    page = page.replace(html, new_css)
    return page


# deletes html of given class
def delete_class(page, html, css):
    page = page.replace(css, "")
    page = page.replace(html, "")
    return page


def create_ready_class(type, html, css):
    global classes

    new_class = 0
    if type == 'text':
        new_class = 'p0'
        for i in range(len(classes) - 1, -1, -1):
            if classes[i].startswith("p"):
                new_class = 'p' + str(int(classes[i][1:]) + 1)
                break
    elif type == 'image':
        new_class = 'i0'
        for i in range(len(classes) - 1, -1, -1):
            if classes[i].startswith("i"):
                new_class = 'i' + str(int(classes[i][1:]) + 1)
                break
    if type == 'image':
        css_copy = css
        css = css_copy[:css_copy.find('&')]
        css_img = css_copy[css_copy.find('&') + 3:]
    css = f".{new_class}" + "{\n\t" + css + "}\n"
    html = f"\t<div class={new_class}>\n\t\t{html}\n\t</div>\n"
    if type == 'image':
        css += f".{new_class} img" + "{\n\t" + css_img + "\n}\n"
    return new_class, html, css


def add_ready_class(page, new_class, html, css):
    page = page.replace("</style>", css + '</style>')
    page = page.replace("</body>", html + '</body>')
    classes.append(new_class)
    return page


# clears form on init or adding any element
def clear_form():
    st.session_state.form_data = [{
        'text': '',
        'color': '#ffffff',
        'noBg': True,
        'bgColor': '#ffffff',
        'isBold': False,
        'isItalic': False,
        'isUnder': False,
        'size': 16,
        'align': "left",
        'align-index': 0,
    }, {
        'url': '',
        'native': True,
        'rt': "px",
        'rt-index': 0,
        'keep_props': True,
        'orig_w': 1,
        'orig_h': 1,
        'res-w': 400,
        'res-h': 400,
        'res-wp': 100,
        'res-hp': 100,
        'align': "left",
        'align-index': 0,
    }, {
        'frame': False,
        'width': 100,
        'align': "fleft",
        'align-index': 0,
        'padding': 20,
        'noBg': True,
        'bg': '#ffffff',
        'border': True,
        'thick': 2,
        'round': 10,
        'borderColor': '#000000'
    }]


# init
if 'type' not in st.session_state:
    st.session_state.type = 'text'

if 'form_data' not in st.session_state:
    clear_form()

if 'edit_mode' not in st.session_state or st.session_state.editing_class is None:
    st.session_state.edit_mode = False
if not st.session_state.edit_mode:
    if st.session_state.type == 'text':
        st.session_state.header = "Add text"
    if st.session_state.type == 'image':
        st.session_state.header = "Add image"

if 'choose_element' not in st.session_state:
    st.session_state.choose_element = False
if 'not_working' not in st.session_state:
    st.session_state.not_working = False
if 'custom_elements' not in st.session_state or st.session_state.not_working:
    st.session_state.custom_elements = None

if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = None
if 'editing_class' not in st.session_state:
    st.session_state.editing_class = None

# interface
st.header("HTML constructor")

# adding buttons
with st.container(border=True):
    col1, col2, col3, space, col4 = st.columns([1, 1.2, 2.2, 11.8, 2])
    add_text = col1.button("Add text")
    add_image = col2.button("Add image")
    custom_el = col3.button("Choose custom element")
    download = col4.download_button(label="Download HTML code", data=st.session_state.input_page, file_name="page.html",
                                    mime='text/html')

# main gui
with st.container():
    explorer, scene, inspector = st.columns([2, 6, 3], gap="medium")
    # a field with all classes in proj
    with explorer:
        with st.container(height=685, border=True):
            st.subheader("Explorer")
            with st.container(height=480, border=False):
                for i, label in enumerate(classes):
                    if st.button(label, key=label):
                        st.session_state.button_pressed = label

            if st.session_state.button_pressed:
                editing = st.session_state.button_pressed
                st.session_state.editing_class = editing
                st.session_state.button_pressed = None

            if st.session_state.editing_class is None:
                st.subheader("Class isn't selected")
            else:
                st.subheader("Selected class: " + st.session_state.editing_class)

            with st.container():
                edit, delete = st.columns(2)
                if st.session_state.editing_class is None:
                    edit = edit.button("Edit", disabled=True)
                    delete = delete.button("Delete", disabled=True)
                else:
                    edit = edit.button("Edit")
                    delete = delete.button("Delete")
    # page
    with scene:
        with st.container(height=685, border=True):
            components.html(st.session_state.input_page, height=645, scrolling=True)

    # form with element's parameters
    with inspector:
        with st.container(height=685, border=True):
            if not st.session_state.choose_element:
                st.subheader(st.session_state.header)
                if st.session_state.type == 'text':
                    text_to_add = st.text_input("text to add", value=st.session_state.form_data[0]['text'])
                    color_text = st.color_picker("color of text", value=st.session_state.form_data[0]['color'])
                    isBold = st.checkbox("Bold", value=st.session_state.form_data[0]['isBold'])
                    isItalic = st.checkbox("Italic", value=st.session_state.form_data[0]['isItalic'])
                    isUnder = st.checkbox("Underlined", value=st.session_state.form_data[0]['isUnder'])
                    text_size = st.number_input("Enter text size", min_value=1, max_value=96,
                                                value=st.session_state.form_data[0]['size'])
                    alignment = st.selectbox("Select text alignment", ["left", "center", "right"],
                                             index=st.session_state.form_data[0]['align-index'],
                                             key=st.session_state.form_data[0]['align'])

                elif st.session_state.type == 'image':
                    image_url = st.text_input("url of image", value=st.session_state.form_data[1]['url'])
                    if is_image_url(image_url):
                        get_image_dimensions(image_url)
                        col1, col2 = st.columns(2)
                        isNative = col1.checkbox("native size", value=st.session_state.form_data[1]['native'])
                        if isNative:
                            st.session_state.form_data[1]['res-w'] = st.session_state.form_data[1]['orig-w']
                            st.session_state.form_data[1]['res-h'] = st.session_state.form_data[1]['orig-h']
                            st.session_state.form_data[1]['res-wp'] = 100
                            st.session_state.form_data[1]['res-hp'] = 100
                            st.session_state.form_data[1]['keep_props'] = True
                        resolution_type = col2.selectbox("set size type", ["px", "%"],
                                                         index=st.session_state.form_data[1]['rt-index'],
                                                         key=st.session_state.form_data[1]['rt'], disabled=isNative)
                        col3, col4, col5 = st.columns(3)

                        keepProps = col1.checkbox("keep proportions", value=st.session_state.form_data[1]['keep_props'],
                                                  disabled=isNative)
                        if keepProps:
                            dimension = col4.selectbox("Select dimension to adjust", ["Width", "Height"])
                            if resolution_type == '%':
                                prop = st.session_state.form_data[1]['res-wp'] / st.session_state.form_data[1]['res-hp']
                                if dimension == "Width":
                                    resolution_width = col5.number_input("width", min_value=1, max_value=200,
                                                                         value=st.session_state.form_data[1]['res-wp'],
                                                                         disabled=isNative)
                                    st.session_state.form_data[1]['res-wp'] = resolution_width
                                    st.session_state.form_data[1]['res-hp'] = round(
                                        st.session_state.form_data[1]['res-wp'] / prop)
                                else:
                                    resolution_height = col5.number_input("height", min_value=1, max_value=200,
                                                                          value=st.session_state.form_data[1]['res-hp'],
                                                                          disabled=isNative)
                                    st.session_state.form_data[1]['res-hp'] = resolution_height
                                    st.session_state.form_data[1]['res-wp'] = round(
                                        st.session_state.form_data[1]['res-hp'] * prop)
                                st.session_state.form_data[1]['res-w'] = round(
                                    st.session_state.form_data[1]['orig-w'] * st.session_state.form_data[1][
                                        'res-wp'] / 100)
                                st.session_state.form_data[1]['res-h'] = round(
                                    st.session_state.form_data[1]['orig-h'] * st.session_state.form_data[1][
                                        'res-hp'] / 100)
                            else:
                                prop = st.session_state.form_data[1]['res-w'] / st.session_state.form_data[1]['res-h']
                                if dimension == "Width":
                                    resolution_width = col5.number_input("width", min_value=1, max_value=5000,
                                                                         value=st.session_state.form_data[1]['res-w'],
                                                                         disabled=isNative)
                                    st.session_state.form_data[1]['res-w'] = resolution_width
                                    st.session_state.form_data[1]['res-h'] = round(
                                        st.session_state.form_data[1]['res-w'] / prop)
                                else:
                                    resolution_height = col5.number_input("height", min_value=1, max_value=5000,
                                                                          value=st.session_state.form_data[1]['res-h'],
                                                                          disabled=isNative)
                                    st.session_state.form_data[1]['res-h'] = resolution_height
                                    st.session_state.form_data[1]['res-w'] = round(
                                        st.session_state.form_data[1]['res-h'] * prop)
                                st.session_state.form_data[1]['res-wp'] = round(
                                    st.session_state.form_data[1]['res-w'] / st.session_state.form_data[1][
                                        'orig-w'] * 100)
                                st.session_state.form_data[1]['res-hp'] = round(
                                    st.session_state.form_data[1]['res-h'] / st.session_state.form_data[1][
                                        'orig-h'] * 100)
                        else:
                            if resolution_type == '%':
                                resolution_width = col4.number_input("width", min_value=1, max_value=200,
                                                                     value=st.session_state.form_data[1]['res-wp'],
                                                                     disabled=isNative)
                                resolution_height = col5.number_input("height", min_value=1, max_value=200,
                                                                      value=st.session_state.form_data[1]['res-hp'],
                                                                      disabled=isNative)
                                st.session_state.form_data[1]['res-wp'] = resolution_width
                                st.session_state.form_data[1]['res-hp'] = resolution_height
                                st.session_state.form_data[1]['res-w'] = round(
                                    st.session_state.form_data[1]['orig-w'] * st.session_state.form_data[1][
                                        'res-wp'] / 100)
                                st.session_state.form_data[1]['res-h'] = round(
                                    st.session_state.form_data[1]['orig-h'] * st.session_state.form_data[1][
                                        'res-hp'] / 100)
                            else:
                                resolution_width = col4.number_input("width", min_value=1, max_value=5000,
                                                                     value=st.session_state.form_data[1]['res-w'],
                                                                     disabled=isNative)
                                st.session_state.form_data[1]['res-w'] = resolution_width
                                resolution_height = col5.number_input("height", min_value=1, max_value=5000,
                                                                      value=st.session_state.form_data[1]['res-h'],
                                                                      disabled=isNative)
                                st.session_state.form_data[1]['res-h'] = resolution_height
                                st.session_state.form_data[1]['res-wp'] = round(
                                    st.session_state.form_data[1]['res-w'] / st.session_state.form_data[1][
                                        'orig-w'] * 100)
                                st.session_state.form_data[1]['res-hp'] = round(
                                    st.session_state.form_data[1]['res-h'] / st.session_state.form_data[1][
                                        'orig-h'] * 100)

                        alignment = st.selectbox("Select image alignment", ["left", "center", "right"],
                                                 index=st.session_state.form_data[1]['align-index'],
                                                 key=st.session_state.form_data[1]['align'])
                    else:
                        if image_url == '':
                            st.write("Url field is empty")
                        else:
                            st.write("It's invalid url")

                isFrame = st.checkbox("Add frame", value=st.session_state.form_data[2]['frame'])
                if isFrame:
                    if st.session_state.type == 'text':
                        width = st.slider("Width", min_value=1, max_value=100,
                                          value=st.session_state.form_data[2]['width'])
                    elif st.session_state.type == 'image':
                        if resolution_type == "px":
                            st.session_state.form_data[2]['width'] = st.session_state.form_data[1]['res-w']
                            width = st.slider("Width", min_value=st.session_state.form_data[1]['res-w'], max_value=5000,
                                              value=st.session_state.form_data[2]['width'])
                        else:
                            st.session_state.form_data[2]['width'] = st.session_state.form_data[1]['res-wp']
                            width = st.slider("Width", min_value=st.session_state.form_data[1]['res-wp'], max_value=200,
                                              value=st.session_state.form_data[2]['width'])
                    frame_alignment = st.selectbox("Select frame alignment", ["left", "center", "right"],
                                                   index=st.session_state.form_data[2]['align-index'],
                                                   key=st.session_state.form_data[2]['align'])
                    padding = st.slider("Padding", min_value=1, max_value=200,
                                        value=st.session_state.form_data[2]['padding'])
                    col6, col7 = st.columns(2)
                    isNoBg = col6.checkbox("no background", value=st.session_state.form_data[2]['noBg'])
                    background = col7.color_picker("background color", value=st.session_state.form_data[2]['bg'],
                                                   disabled=isNoBg)

                    col8, col9 = st.columns(2)
                    hasBorder = col8.checkbox("Add border", value=st.session_state.form_data[2]['border'])
                    borderColor = col9.color_picker("Border color", value=st.session_state.form_data[2]['borderColor'],
                                                    disabled=not hasBorder)
                    thickness = st.slider("Border thickness", min_value=0, max_value=20,
                                          value=st.session_state.form_data[2]['thick'], disabled=not hasBorder)
                    rounding = st.slider("Border rounding", min_value=0, max_value=20,
                                         value=st.session_state.form_data[2]['round'], disabled=not hasBorder)

                if st.session_state.type == 'image':
                    submit = st.button("Submit", disabled=not is_image_url(image_url))
                else:
                    submit = st.button("Submit")
                if submit:
                    if not st.session_state.edit_mode:
                        st.session_state.input_page = add_class(st.session_state.input_page, st.session_state.type)
                        clear_form()
                        st.rerun()
                    else:
                        st.session_state.input_page = edit_class(st.session_state.input_page, st.session_state.type,
                                                                 st.session_state.editing_class)
                        st.rerun()

            else:
                if not st.session_state.not_working and st.session_state.custom_elements is not None:
                    for i in range(1, len(st.session_state.custom_elements) + 1):
                        with st.container(border=True):
                            new_class, html, css = create_ready_class(st.session_state.custom_elements[i - 1]['type'],
                                                                      st.session_state.custom_elements[i - 1][
                                                                          'html_content'],
                                                                      st.session_state.custom_elements[i - 1][
                                                                          'css_content'])
                            st.subheader('Preview')
                            st.components.v1.html(html=f'<style>\n{css}\n</style>\n<body>\n{html}\n</body>', width=390,
                                                  scrolling=True)
                            if st.button('Add', key=i):
                                new_class, html, css = create_ready_class(
                                    st.session_state.custom_elements[i - 1]['type'],
                                    st.session_state.custom_elements[i - 1]['html_content'],
                                    st.session_state.custom_elements[i - 1]['css_content'])
                                st.session_state.input_page = add_ready_class(st.session_state.input_page, new_class,
                                                                              html, css)
                                st.rerun()
                elif st.session_state.not_working:
                    st.subheader("This module doesn't work now")
                else:
                    st.subheader("There are no elements yet")

# button pressing checks
if delete:
    if st.session_state.editing_class is not None:
        html, css = find_html_and_css(st.session_state.input_page, st.session_state.editing_class)
        st.session_state.input_page = delete_class(st.session_state.input_page, html, css)
        if st.session_state.editing_class.startswith('i'):
            html, css = find_html_and_css(st.session_state.input_page, st.session_state.editing_class + ' img')
            st.session_state.input_page = delete_class(st.session_state.input_page, html, css)
        st.session_state.editing_class = None
        st.session_state.edit_mode = False
        clear_form()
        st.rerun()

if edit:
    if st.session_state.editing_class is not None:
        st.session_state.header = f"Edit {st.session_state.editing_class}"
        if st.session_state.editing_class.startswith("p"):
            st.session_state.type = 'text'
        elif st.session_state.editing_class.startswith("i"):
            st.session_state.type = 'image'
        get_class_params(st.session_state.input_page, st.session_state.editing_class, st.session_state.type)
        st.session_state.edit_mode = True
        st.session_state.choose_element = False
        st.rerun()

if add_text:
    st.session_state.type = 'text'
    st.session_state.editing_class = None
    st.session_state.choose_element = False
    clear_form()
    st.rerun()

if add_image:
    st.session_state.type = 'image'
    st.session_state.editing_class = None
    st.session_state.choose_element = False
    clear_form()
    st.rerun()

if custom_el:
    st.session_state.choose_element = True
    st.session_state.custom_elements = fetch_components()
    clear_form()
    st.rerun()
