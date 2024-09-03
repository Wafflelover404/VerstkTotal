import json
import streamlit as st
from code_editor import code_editor
import base64
import sqlite3
import streamlit.components.v1 as components
from login import get_user_id_by_username
from login import get_file_ids_by_user_id
from login import get_file_data_as_json

# Initialize session state variables
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
if 'account' not in st.session_state:
    st.session_state.account = ""
if 'show_ai_coder' not in st.session_state:
    st.session_state.show_ai_coder = False

# Load custom buttons and CSS
with open('resources/example_custom_buttons_bar_alt.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)
with open('resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)
with open('resources/example_code_editor_css.scss') as css_file:
    css_text = css_file.read()

# Construct component props dictionary
comp_props = {"css": css_text, "globalCSS": ":root {\n  --streamlit-dark-font-family: monospace;\n}"}

mode_list = ["abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "bibtex", "c9search", "c_cpp", "cirru", "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot", "drools", "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", "io", "ion", "jack", "jade", "java", "javascript", "jexl", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", "kotlin", "latex", "latte", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mips", "mixal", "mushcode", "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "partiql", "pascal", "perl", "pgsql", "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", "properties", "protobuf", "puppet", "python", "qml", "r", "raku", "razor", "rdoc", "red", "redshift", "rhtml", "robot", "rst", "ruby", "rust", "sac", "sass", "scad", "scala", "scheme", "scrypt", "scss", "sh", "sjs", "slim", "smarty", "smithy", "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", "terraform", "tex", "text", "textile", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", "velocity", "verilog", "vhdl", "visualforce", "wollok", "xml", "xquery", "yaml", "zeek"]

btns = custom_buttons_alt

st.title("VerstkEdit")
st.markdown("A simple website editor")

upload, load = st.columns([3, 3])

with upload:
    with st.container(border=True, height=325):
        uploaded_file = st.file_uploader(label="Choose your HTML file.", label_visibility="collapsed")
        st.subheader("Or")
        st.write("Use generator, constructor")
        st.subheader("Or")
        if st.button("Create new file"):
            st.session_state.edited_content = ""
        

with load:
    with st.container(border=True, height=325):
        if st.session_state.account:
            with sqlite3.connect(st.session_state.db_path) as db:
                    cursor = db.cursor()
                    user_id = get_user_id_by_username(cursor, st.session_state.account)
                    file_ids = get_file_ids_by_user_id(cursor, user_id)
                    
                    if file_ids:
                        # Create tabs for each file ID
                        tabs = [f"File ID: {file_id}" for file_id in file_ids]
                        selected_tab = st.tabs(tabs)
                        
                        for file_id, tab_name in zip(file_ids, tabs):
                            with selected_tab[tabs.index(tab_name)]:
                                file_json_str = get_file_data_as_json(cursor, file_id)
                                file_json = json.loads(file_json_str)  # Parse the JSON string into a dictionary
                                st.write(f"**Filename**: {file_json['filename']}")
                                st.write("**File contents:**")
                                with st.expander("View source code"):
                                    st.code(file_json["content"], line_numbers=True)
                                if st.button(label="Edit", help="Open this file in code editor", key=f"{file_id}_export"):
                                    st.session_state.edited_content = file_json["content"]
                                    st.success("Opened in Web Editor !")
                    else:
                        st.write("No files found for this user.")
        else:
            st.warning("Login to load project from account")

if uploaded_file is not None:
    st.session_state.uploaded_file_content = uploaded_file.read().decode('utf-8')
    st.session_state.edited_content = st.session_state.uploaded_file_content

if st.session_state.edited_content is not None:
    bytes_data = st.session_state.edited_content
    st.write("filename:", uploaded_file.name if uploaded_file else "Not defined")

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
        
        # Render code editor
        ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
        response_dict = code_editor(bytes_data, height=st.session_state.height, lang=st.session_state.language, theme=st.session_state.theme, shortcuts=st.session_state.shortcuts, focus=st.session_state.focus, buttons=btns, info=info_bar, props=ace_props, options={"wrap": st.session_state.wrap}, allow_reset=True, key="code_editor_demo")    

        # Initial tabs
        tabs = ["Save", "Download", "AI coder", "Code result"]

        # Create tabs
        tab_objects = st.tabs(tabs)

        # Assign tabs to variables
        tab_save = tab_objects[tabs.index("Save")]
        tab_download = tab_objects[tabs.index("Download")]
        tab_ai_coder = tab_objects[tabs.index("AI coder")]
        tab_code_result = tab_objects[tabs.index("Code result")]
            
        # Save Tab
        with tab_download:
            filename = st.text_input(label="Enter filename", key='filename2')
            if st.download_button(
                label="Export",
                data=st.session_state.get('edited_content', ''),
                file_name=filename,
                key="Download"
            ):
                st.success("Download started!")
            
            # Download Tab
            with tab_save:
                if st.session_state.get('account', ''):
                    filename = st.text_input(label="Enter filename", key='filename1')
                    if st.button(label="Submit"):
                        with sqlite3.connect(st.session_state.db_path) as db:
                            cursor = db.cursor()
                            cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, st.session_state.get('edited_content', '')))
                            file_id = cursor.lastrowid
                            cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (st.session_state.account_id, file_id))
                            db.commit()
                            st.success(f"File added to the database with file_id: {file_id}")
                            st.success("Saved to your account. Visit the login page to see.")
                else:
                    st.error("Login to save your files.")
                    
        with tab_ai_coder:
            # This code is a merge of assistant.py and compare.py, using both 

            context = False

            diff_result = ""
            st.header("VerstkEdit Ai test.")
            UserCode = st.session_state.edited_content

            css = st.markdown("""
            <style>
                .st-da st-db st-dc st-f3 st-gp st-gq st-gr st-gs st-gt st-gu st-hc st-cc st-bb st-he st-gx st-gy st-gz st-h0 st-eu st-h1 st-fi st-h2 st-c3 st-c4 st-c5 st-c6 st-h3 st-h4 st-h5 st-h6 st-c7 st-c8 st-c9 st-ca st-h7 st-h8 st-h9 st-ha {
                    width: 100%;
                }

                .st-emotion-cache-15hul6a ef3psqc12 {
                    width: 100%;
                }       
            </style>
            """, unsafe_allow_html=True)

            def st_codemirror_diff(left, right, opts, key=None): # This function is used to compare Ai-written code with user's one.
                    # Generate a diff using difflib
                    diff = difflib.unified_diff(
                        left.splitlines(keepends=True),
                        right.splitlines(keepends=True),
                        fromfile='Left',
                        tofile='Right',
                    )
                    diff_result = ''.join(diff)
                    return diff_result

            opts = { # Options for difference
                "mode": "python",
                "theme": "default",
            }

            def send(request, hf_token): # This function is used for sending request (Forked from assistant.py).
                API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
                headers = {"Authorization": f"Bearer {hf_token}"}

                def query(payload):
                    response = requests.post(API_URL, headers=headers, json=payload)
                    return response.json()

                def replace_assistant(strin):
                    e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
                    e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
                    return e.strip()

                prompt = f"""
                    <|system|>
                    Assistant is an expert in coding. He is specialized in frontend web development. He has to help user by writing code only. RESPOND WITH HTML CODE ONLY.
                    </s>
                    <|user|>
                    {request}
                    </s>
                    <|assistant|>
                    """
                
                for _ in range(10):
                    try:
                        response = query({
                            "inputs": prompt,
                            "parameters": {"max_new_tokens": 8000, "use_cache": False, "max_time": 120.0},
                            "options": {"wait_for_model": True}
                        })
                        full_response = replace_assistant(response[0]["generated_text"])
                        return full_response
                    except Exception as e:
                        print(e)
                        continue
                
                return "Error"

            # Here starts the streamlit interface for Ai assistant
            if 'hf_token' not in st.session_state:
                st.session_state.hf_token = ""

            st.markdown("Ask the assistant any coding-related questions. The assistant has your code as context for your request.")
            context = st.checkbox("Code context", help="Tick the checkbox to let Ai see your code.")    
            request = st.text_area(label="")
            try:
                if context:
                    request = f"""
                        User's request: {request}

                        User's code: {UserCode}
                    """
                else:
                    request = f"""
                        User's request: {request}
                    """
                response = send(request, st.session_state.hf_token)
                if response != "Error":
                    print("Text writing successfully!", response)
                    st.write(f"Ai response finished !")
                    # Display the difference result between user's code and ai's
                    diff_result = st_codemirror_diff(UserCode, response, opts)
                else:
                    print("An error occurred while communicating with TextAi.")
            except Exception as e:
                print(f"An error occurred: {e}")
                

        if diff_result is not None and diff_result is not "":
            st.subheader("Diff Result")
            st.code(diff_result, language='diff')
            st.header("Page preview")
            st.components.v1.html(response)
        
        # Code Result Tab (conditionally rendered)
        if 'response_dict' in locals() and response_dict.get('type') == "submit":
            with tab_code_result:
                st.header("Page preview")
                st.components.v1.html(response_dict['text'], height=750)
                st.session_state.edited_content = response_dict['text']