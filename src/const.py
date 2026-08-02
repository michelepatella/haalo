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

UPLOAD_PAGE_DISCLAIMER = (
    "💡 **Haalo** is an AI chatbot designed to help you understand academic documents. "
    "Other document types may produce suboptimal results."
)

UPLOAD_PAGE_STYLE_PATH = Path("assets/styles/upload.css")

#########################################################################################
# Preprocess Page
#########################################################################################
PREPROCESS_PAGE_SPINNER_MESSAGE = "Processing document..."

PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW = [1, 2, 1]

PREPROCESS_PAGE_STYLE_PATH = Path("assets/styles/preprocess.css")

#########################################################################################
# Embedding
#########################################################################################
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

#########################################################################################
# Vector Store
#########################################################################################
VECTOR_STORE_COLLECTION_NAME = "haalo_collection"
VECTOR_STORE_PERSIST_DIR = "./haalo_db"

#########################################################################################
# Session State
#########################################################################################
SESSION_STATE_UPLOADED_DOC_PATH_KEY = "uploaded_doc_path"
SESSION_STATE_INDEX_KEY = "index"
