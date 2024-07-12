import streamlit as st
import difflib

st.set_page_config(layout="centered")

with st.popover("Compare code"):
    st.markdown("<style>* { width: 100%}</style>", unsafe_allow_html=True)
    st.title("Code Comparison by Wafflelover404")

    def st_codemirror_diff(left, right, opts, key=None):
        # Generate a diff using difflib
        diff = difflib.unified_diff(
            left.splitlines(keepends=True),
            right.splitlines(keepends=True),
            fromfile='Left',
            tofile='Right',
        )
        diff_result = ''.join(diff)
        return diff_result

    inp1, inp2 = st.columns(2)

    with inp1:  
        left_code = st.text_area("1st code")

    with inp2:
        right_code = st.text_area("2nd code")

    opts = {
        "mode": "python",
        "theme": "default",
    }

    # Create two columns
    col1, col2 = st.columns(2)

    # Display left code in the first column
    with col1:
        st.subheader("Left Code")
        st.code(left_code, language='python')

    # Display right code in the second column
    with col2:
        st.subheader("Right Code")
        st.code(right_code, language='python')

    # Optionally, display the diff result
    diff_result = st_codemirror_diff(left_code, right_code, opts)
    if diff_result is not None:
        st.subheader("Diff Result")
        st.code(diff_result, language='diff')
    else:
        st.warning("Failed to load the diff component. Please check the URL or local build.")