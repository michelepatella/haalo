"""src/const.py"""

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
    "💡 Haalo is an AI chatbot designed to help you understand academic documents. "
    "Other document types may produce suboptimal results."
)

UPLOAD_PAGE_ERROR_MESSAGE = (
    "Something went wrong while uploading your document."
)

UPLOAD_PAGE_STYLE_PATH = Path("assets/styles/upload.css")

#########################################################################################
# Preprocess Page
#########################################################################################
PREPROCESS_PAGE_SPINNER_MESSAGE = "Processing document..."

PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW = [1, 2, 1]

PREPROCESS_PAGE_ERROR_MESSAGE = (
    "Something went wrong while processing your document."
)

PREPROCESS_PAGE_STYLE_PATH = Path("assets/styles/preprocess.css")

#########################################################################################
# Chat Page
#########################################################################################
CHAT_PAGE_INPUT_PLACEHOLDER = "Ask something about your document..."

CHAT_PAGE_RESET_CONVERSATION_BUTTON_LABEL = "Reset Conversation"
CHAT_PAGE_UPLOAD_NEW_DOCUMENT_BUTTON_LABEL = "Upload New Document"

CHAT_PAGE_SOURCES_TITLE = "Sources"

CHAT_PAGE_SPINNER_MESSAGE = "Generating response..."

CHAT_PAGE_MESSAGE_ROLE_KEY = "role"
CHAT_PAGE_MESSAGE_CONTENT_KEY = "content"
CHAT_PAGE_MESSAGE_SOURCES_KEY = "sources"

CHAT_PAGE_RESPONSE_SOURCE_NODES_KEY = "source_nodes"

CHAT_PAGE_MESSAGE_ROLE_USER = "user"
CHAT_PAGE_MESSAGE_ROLE_ASSISTANT = "assistant"

CHAT_PAGE_ASSISTANT_AVATAR = "💡"
CHAT_PAGE_USER_AVATAR = "👤"

CHAT_PAGE_STYLE_PATH = Path("assets/styles/chat.css")

#########################################################################################
# Vector Store
#########################################################################################
VECTOR_STORE_COLLECTION_NAME = "haalo_collection"

#########################################################################################
# Session State
#########################################################################################
SESSION_STATE_UPLOADED_DOC_PATH_KEY = "uploaded_doc_path"
SESSION_STATE_INDEX_KEY = "index"
SESSION_STATE_CHAT_ENGINE_KEY = "chat_engine"
SESSION_STATE_MESSAGE_HISTORY_KEY = "message_history"

#########################################################################################
# System Prompt
#########################################################################################
SYSTEM_PROMPT = """You are an AI assistant designed to help users analyze and query their uploaded documents.

INSTRUCTIONS:
1. Answer the question STRICTLY using ONLY the information provided in the context.
2. If the user's question cannot be answered using the provided context, or if it is out-of-topic, you MUST reply: "I cannot answer this question because the information is not present in the uploaded document."
3. Do NOT use your own background knowledge to answer.
"""
