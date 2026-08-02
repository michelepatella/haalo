"""src/main.py"""

import streamlit as st

import chat
import preprocess
import upload
from const import (
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
    SESSION_STATE_INDEX_KEY,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
)

# Streamlit app configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
)

# Initialize session states
if SESSION_STATE_UPLOADED_DOC_PATH_KEY not in st.session_state:
    st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] = None
if SESSION_STATE_INDEX_KEY not in st.session_state:
    st.session_state[SESSION_STATE_INDEX_KEY] = None

# Navigate between pages based on session states
if st.session_state[SESSION_STATE_INDEX_KEY] is not None:
    # Chat page (document has been processed and is ready for RAG)
    chat.render_chat_page(st.session_state[SESSION_STATE_INDEX_KEY])
elif st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] is not None:
    # Preprocess page (document has been uploaded and is ready to be processed)
    preprocess.render_preprocess_page(
        st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY],
    )
else:
    # Upload page (document has not been uploaded yet)
    upload.render_upload_page()
