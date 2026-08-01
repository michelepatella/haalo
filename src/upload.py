"""src/upload.py"""

import tempfile

import streamlit as st

from const import (
    LOGO_PATH,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
    UPLOAD_PAGE_COLUMN_LAYOUT_NARROW,
    UPLOAD_PAGE_COLUMN_LAYOUT_WIDE,
    UPLOAD_PAGE_FILE_UPLOADER_LABEL,
    UPLOAD_PAGE_FILE_UPLOADER_LABEL_VISIBILITY,
    UPLOAD_PAGE_HEADER,
    UPLOAD_PAGE_PROCEED_BUTTON_LABEL,
    UPLOAD_PAGE_STYLE_PATH,
    UPLOAD_PAGE_SUBHEADER,
    UPLOAD_PAGE_UPLOADED_DOC_FORMAT,
)


def render_upload_page() -> None:
    """Render the upload page for the Streamlit app.

    This function displays the logo, header, and subheader, and applies
    custom CSS styling to the upload page.

    Returns:
        None
    """
    # Logo
    _, col_img, _ = st.columns(UPLOAD_PAGE_COLUMN_LAYOUT_WIDE)
    with col_img:
        st.image(LOGO_PATH)

    # Header and subheader
    st.markdown(
        f"<h2 align='center'>{UPLOAD_PAGE_HEADER}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p align='center'>{UPLOAD_PAGE_SUBHEADER}</p>",
        unsafe_allow_html=True,
    )

    # Custom CSS
    with open(UPLOAD_PAGE_STYLE_PATH) as f:
        css = f.read()

    st.markdown(
        f"""<style>{css}</style>""",
        unsafe_allow_html=True,
    )

    # Upload the academic document
    uploaded_doc_path = _upload_academic_document()

    # If a document is uploaded, display a button to proceed
    if uploaded_doc_path is not None:
        _, col_btn, _ = st.columns(UPLOAD_PAGE_COLUMN_LAYOUT_NARROW)
        with col_btn:
            if st.button(UPLOAD_PAGE_PROCEED_BUTTON_LABEL):
                st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] = (
                    uploaded_doc_path
                )
                st.rerun()


def _save_file_to_temp(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
) -> str:
    """Save an uploaded file to a temporary location on disk.

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
        delete=False,
        suffix=f".{UPLOAD_PAGE_UPLOADED_DOC_FORMAT}",
    ) as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name


def _upload_academic_document() -> str | None:
    """Upload an academic document.

    This function provides a file uploader for users to upload an
    academic document.

    Returns:
        str | None:
            The path to the uploaded document if successful, or None if no
            file was uploaded.
    """
    _, col_content, _ = st.columns(UPLOAD_PAGE_COLUMN_LAYOUT_NARROW)
    with col_content:
        # File uploader
        uploaded_file = st.file_uploader(
            UPLOAD_PAGE_FILE_UPLOADER_LABEL,
            type=UPLOAD_PAGE_UPLOADED_DOC_FORMAT,
            label_visibility=UPLOAD_PAGE_FILE_UPLOADER_LABEL_VISIBILITY,
        )

        # If a file is uploaded, save it to a temporary
        # file and return the path
        if uploaded_file is not None:
            return _save_file_to_temp(uploaded_file)

    return None
