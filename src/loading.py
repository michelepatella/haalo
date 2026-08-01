"""src/loading.py"""

import tempfile
import streamlit as st
from const import (
    LOGO_PATH,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
    LOADING_PAGE_HEADER,
    LOADING_PAGE_SUBHEADER,
    LOADING_PAGE_COLUMN_LAYOUT_NARROW,
    LOADING_PAGE_COLUMN_LAYOUT_WIDE,
    LOADING_PAGE_FILE_UPLOADER_LABEL,
    LOADING_PAGE_FILE_UPLOADER_LABEL_VISIBILITY,
    LOADING_PAGE_UPLOADED_DOC_FORMAT,
    LOADING_PAGE_PROCEED_BUTTON_LABEL,
    LOADING_PAGE_STYLE_PATH,
)


def render_loading_page() -> None:
    """Renders the loading page for the Streamlit app.

    This function displays the logo, header, and subheader, and applies 
    custom CSS styling to the loading page.

    Returns:
        None
    """
    # Logo
    _, col_img, _ = st.columns(LOADING_PAGE_COLUMN_LAYOUT_WIDE)
    with col_img:
        st.image(LOGO_PATH)

    # Header and subheader
    st.markdown(
        f"<h2 align='center'>{LOADING_PAGE_HEADER}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p align='center'>{LOADING_PAGE_SUBHEADER}</p>",
        unsafe_allow_html=True,
    )

    # Custom CSS
    with open(LOADING_PAGE_STYLE_PATH, "r") as f:
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
        delete=False, suffix=f".{LOADING_PAGE_UPLOADED_DOC_FORMAT}"
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
    _, col2, _ = st.columns(LOADING_PAGE_COLUMN_LAYOUT_NARROW)
    with col2:
        # File uploader
        uploaded_file = st.file_uploader(
            LOADING_PAGE_FILE_UPLOADER_LABEL,
            type=LOADING_PAGE_UPLOADED_DOC_FORMAT,
            label_visibility=LOADING_PAGE_FILE_UPLOADER_LABEL_VISIBILITY,
        )

        # If a file is uploaded, save it to a temporary
        # file and return the path
        if uploaded_file is not None:
            return _save_file_to_temp(uploaded_file)

    return None


# Load the academic document
uploaded_doc_path = load_academic_document()

# If a document is loaded, display a button to proceed
if uploaded_doc_path is not None:
    _, col_btn, _ = st.columns(LOADING_PAGE_COLUMN_LAYOUT_NARROW)
    with col_btn:
        if st.button(LOADING_PAGE_PROCEED_BUTTON_LABEL):
            st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] = uploaded_doc_path
            st.rerun()
