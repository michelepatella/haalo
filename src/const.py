from pathlib import Path

########################################################################################
# General
########################################################################################
LOGO_PATH = Path("assets/images/logo.png")

PAGE_TITLE = "Haalo"
PAGE_ICON = "💡"
PAGE_LAYOUT = "wide"

########################################################################################
# Upload Page
########################################################################################
UPLOAD_PAGE_HEADER = "Learn faster. Explore deeper."
UPLOAD_PAGE_SUBHEADER = "🚀 Upload an academic document to start chatting!"

UPLOAD_PAGE_COLUMN_LAYOUT_NARROW = [1, 2, 1]
UPLOAD_PAGE_COLUMN_LAYOUT_WIDE = [3, 2, 3]

UPLOAD_PAGE_FILE_UPLOADER_LABEL = ""
UPLOAD_PAGE_FILE_UPLOADER_LABEL_VISIBILITY = "hidden"

UPLOAD_PAGE_UPLOADED_DOC_FORMAT = "pdf"

UPLOAD_PAGE_PROCEED_BUTTON_LABEL = "Next ➔"

UPLOAD_PAGE_STYLE_PATH = Path("assets/styles/upload.css")

#########################################################################################
# Preprocess Page
#########################################################################################
PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW = [1, 2, 1]

PREPROCESS_PAGE_STYLE_PATH = Path("assets/styles/preprocess.css")

#########################################################################################
# Session State
#########################################################################################
SESSION_STATE_UPLOADED_DOC_PATH_KEY = "uploaded_doc_path"
SESSION_STATE_VECTOR_STORE_KEY = "vector_store"
