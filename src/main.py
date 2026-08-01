"""src/main.py"""

import streamlit as st

import upload
from const import (
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
)

# Streamlit app configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
)

# Initialize session state for uploaded document path
if SESSION_STATE_UPLOADED_DOC_PATH_KEY not in st.session_state:
    st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] = None

# Render the upload page if no document has been uploaded yet
if st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] is None:
    upload.render_upload_page()
