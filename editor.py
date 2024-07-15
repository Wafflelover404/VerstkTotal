import json
import streamlit as st
from code_editor import code_editor
import base64

def auto_download_html(object_to_download, download_filename):
    b64 = base64.b64encode(object_to_download.encode()).decode()
    html = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $(document).ready(function() {{
        var a = document.createElement('a');
        a.href = 'data:text/html;base64,{b64}';
        a.download = '{download_filename}';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }});
    </script>
    </head>
    <body>
    <p>Your download should start automatically. If it doesn't, please <a id="downloadLink" href="data:text/html;base64,{b64}" download="{download_filename}">click here</a>.</p>
    </body>
    </html>
    """
    return html

# Initialize session state
if 'uploaded_file_content' not in st.session_state:
    st.session_state.uploaded_file_content = None
if 'height' not in st.session_state:
    st.session_state.height = [19, 22]
if 'language' not in st.session_state:
    st.session_state.language = "html"
if 'theme' not in st.session_state:
    st.session_state.theme = "default"
if 'shortcuts' not in st.session_state:
    st.session_state.shortcuts = "vscode"
if 'focus' not in st.session_state:
    st.session_state.focus = True
if 'wrap' not in st.session_state:
    st.session_state.wrap = True
if 'edited_content' not in st.session_state:
    st.session_state.edited_content = None

# Load custom buttons from JSON file
with open('resources/example_custom_buttons_bar_alt.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

# Load Info bar CSS from JSON file
with open('resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

# Load Code Editor CSS from file
with open('resources/example_code_editor_css.scss') as css_file:
    css_text = css_file.read()

# Construct component props dictionary (->Code Editor)
comp_props = {"css": css_text, "globalCSS": ":root {\n  --streamlit-dark-font-family: monospace;\n}"}

mode_list = ["abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "bibtex", "c9search", "c_cpp", "cirru", "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot", "drools", "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", "io", "ion", "jack", "jade", "java", "javascript", "jexl", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", "kotlin", "latex", "latte", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mips", "mixal", "mushcode", "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "partiql", "pascal", "perl", "pgsql", "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", "properties", "protobuf", "puppet", "python", "qml", "r", "raku", "razor", "rdoc", "red", "redshift", "rhtml", "robot", "rst", "ruby", "rust", "sac", "sass", "scad", "scala", "scheme", "scrypt", "scss", "sh", "sjs", "slim", "smarty", "smithy", "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", "terraform", "tex", "text", "textile", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", "velocity", "verilog", "vhdl", "visualforce", "wollok", "xml", "xquery", "yaml", "zeek"]

btn_settings_editor_btns = [{
    "name": "copy",
    "feather": "Copy",
    "hasText": True,
    "alwaysOn": True,
    "commands": ["copyAll"],
    "style": {"top": "0rem", "right": "0.4rem"}
  },{
    "name": "update",
    "feather": "RefreshCw",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"bottom": "0rem", "right": "0.4rem"}
  }]

btns = custom_buttons_alt

st.title("VerstkEdit")
st.markdown("A simple website editor")

uploaded_file = st.file_uploader("Choose your HTML file.")

if uploaded_file is not None:
    st.session_state.uploaded_file_content = uploaded_file.read().decode('utf-8')
    st.session_state.edited_content = st.session_state.uploaded_file_content

if st.session_state.edited_content is not None:
    bytes_data = st.session_state.edited_content
    st.write("filename:", uploaded_file.name if uploaded_file else "Unknown")
    st.write("Original content:")

    st.write("")
    with st.expander("Settings", expanded=True):
        col_a, col_b, col_c, col_cb = st.columns([6,11,3,3])
        col_c.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)
        col_cb.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)

        height_type = col_a.selectbox("height format:", ["min-max lines"])
        if height_type == "min-max lines":
            st.session_state.height = col_b.slider("min-max lines:", 1, 40, st.session_state.height)

        col_d, col_e, col_f = st.columns([1,1,1])
        st.session_state.language = col_d.selectbox("lang:", mode_list, index=mode_list.index(st.session_state.language))
        st.session_state.theme = col_e.selectbox("theme:", ["default", "light", "dark", "contrast"], index=["default", "light", "dark", "contrast"].index(st.session_state.theme))
        st.session_state.shortcuts = col_f.selectbox("shortcuts:", ["emacs", "vim", "vscode", "sublime"], index=["emacs", "vim", "vscode", "sublime"].index(st.session_state.shortcuts))
        st.session_state.focus = col_c.checkbox("focus", st.session_state.focus)
        st.session_state.wrap = col_cb.checkbox("wrap", st.session_state.wrap)

    # Construct props dictionary (->Ace Editor)
    ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
    response_dict = code_editor(bytes_data,  height=st.session_state.height, lang=st.session_state.language, theme=st.session_state.theme, shortcuts=st.session_state.shortcuts, focus=st.session_state.focus, buttons=btns, info=info_bar, props=ace_props, options={"wrap": st.session_state.wrap}, allow_reset=True, key="code_editor_demo")

    if len(response_dict['id']) != 0 and (response_dict['type'] == "selection"):
        st.write(response_dict)
    
    if len(response_dict['id']) != 0 and (response_dict['type'] == "submit"):
        print(response_dict)
        print("Running !!!")
        st.header("Page preview")
        st.components.v1.html(response_dict['text'], height=750)
        st.session_state.edited_content = response_dict['text']

    if response_dict['type'] == "saved":
        print("Downloading !!!")
        st.components.v1.html(auto_download_html(response_dict['text'], "output.html"), height=0, width=0)