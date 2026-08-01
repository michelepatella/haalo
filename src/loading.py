"""src/loading.py"""

import tempfile
import streamlit as st


################################################
# Constants
################################################
PAGE_TITLE = "Haalo"
PAGE_ICON = "💡"
PAGE_LAYOUT = "wide"

PAGE_HEADER = "Learn faster. Explore deeper."
PAGE_SUBHEADER = "🚀 Upload an academic document to start chatting!"

UPLOADER_LABEL = ""
UPLOADER_LABEL_VISIBILITY = "hidden"

DOC_FORMAT = ".pdf"

PROCEED_BUTTON_LABEL = "Next ➔"

SESSION_STATE_DOC_PATH_KEY = "doc_path"

COLUMN_LAYOUT_NARROW = [1, 2, 1]
COLUMN_LAYOUT_WIDE = [3, 2, 3]

LOGO_PATH = "assets/images/logo.png"
STYLE_PATH = "assets/styles/loading.css"


################################################
# Streamlit App Configuration
################################################

# Page Configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
)

# Logo
_, col_img, _ = st.columns(COLUMN_LAYOUT_WIDE)
with col_img:
    st.image(LOGO_PATH)

# Header and Subheader
st.markdown(
    f"<h2 align='center'>{PAGE_HEADER}</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p align='center'>{PAGE_SUBHEADER}</p>",
    unsafe_allow_html=True,
)

# Custom CSS
with open(STYLE_PATH, "r") as f:
    css = f.read()

st.markdown(
    f"""<style>{css}</style>""",
    unsafe_allow_html=True,
)


def _save_file_to_temp(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
) -> str:
    """Saves an uploaded file to a temporary location on disk.

    This function takes a Streamlit UploadedFile object, reads its content,
    and writes it to a temporary file on disk.

    Args:
        uploaded_file (st.runtime.uploaded_file_manager.UploadedFile):
            The Streamlit UploadedFile object.

    Returns:
        str:
            The absolute path to the saved temporary file.
    """
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=DOC_FORMAT
    ) as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name


def load_academic_document() -> str | None:
    """
    Load an academic document.

    This function provides a file uploader for users to load an
    academic document.

    Returns:
        str | None:
            The path to the loaded document if successful, or None if no
            file was uploaded.
    """
    _, col2, _ = st.columns(COLUMN_LAYOUT_NARROW)
    with col2:
        # File uploader
        uploaded_file = st.file_uploader(
            UPLOADER_LABEL,
            type=DOC_FORMAT,
            label_visibility=UPLOADER_LABEL_VISIBILITY,
        )

        # If a file is uploaded, save it to a temporary file and return the path
        if uploaded_file is not None:
            return _save_file_to_temp(uploaded_file)

    return None


# Load the academic document
doc_path = load_academic_document()

# If a document is loaded, display a button to proceed
if doc_path is not None:
    _, col_btn, _ = st.columns(COLUMN_LAYOUT_NARROW)
    with col_btn:
        if st.button(PROCEED_BUTTON_LABEL):
            st.session_state[SESSION_STATE_DOC_PATH_KEY] = doc_path
            st.rerun()
