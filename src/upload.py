"""src/upload.py"""

import tempfile

import streamlit as st

from const import (
    LOGO_PATH,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
    UPLOAD_PAGE_COLUMN_LAYOUT_NARROW,
    UPLOAD_PAGE_COLUMN_LAYOUT_WIDE,
    UPLOAD_PAGE_DISCLAIMER,
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

    This function displays the logo, header, subheader, file uploader,
    and proceed button, applying custom CSS styling to the upload page.

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

    # File uploader
    _, col_content, _ = st.columns(UPLOAD_PAGE_COLUMN_LAYOUT_NARROW)
    with col_content:
        uploaded_file = st.file_uploader(
            UPLOAD_PAGE_FILE_UPLOADER_LABEL,
            type=UPLOAD_PAGE_UPLOADED_DOC_FORMAT,
            label_visibility=UPLOAD_PAGE_FILE_UPLOADER_LABEL_VISIBILITY,
        )

    # If a document is uploaded, display a button to proceed
    if uploaded_file is not None:
        _, col_btn, _ = st.columns(UPLOAD_PAGE_COLUMN_LAYOUT_NARROW)
        with col_btn:
            if st.button(UPLOAD_PAGE_PROCEED_BUTTON_LABEL):
                uploaded_doc_path = _save_file_to_temp(uploaded_file)
                if uploaded_doc_path is not None:
                    st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] = (
                        uploaded_doc_path
                    )
                    st.rerun()
                else:
                    st.error("Error saving file to disk!")

    # Disclaimer
    _, col_disclaimer, _ = st.columns(UPLOAD_PAGE_COLUMN_LAYOUT_NARROW)
    with col_disclaimer:
        st.markdown(
            f"""
            <sub style="display: block; text-align: center;">
                {UPLOAD_PAGE_DISCLAIMER}
            </sub>
            """,
            unsafe_allow_html=True,
        )


def _save_file_to_temp(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
) -> str | None:
    """Save an uploaded file to a temporary location on disk.

    This function takes a Streamlit UploadedFile object, reads its content,
    and writes it to a temporary file on disk.

    Args:
        uploaded_file (st.runtime.uploaded_file_manager.UploadedFile):
            The Streamlit UploadedFile object.

    Returns:
        str | None:
            The absolute path to the saved temporary file, or None if saving failed.
    """
    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{UPLOAD_PAGE_UPLOADED_DOC_FORMAT}",
        ) as temp_file:
            temp_file.write(uploaded_file.read())
            return temp_file.name
    except Exception:
        return None
