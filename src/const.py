"""src/const.py"""

from pathlib import Path

########################################################################################
# App
########################################################################################
APP_TITLE = "Haalo"
APP_ICON = "💡"
APP_LAYOUT = "wide"

APP_LOGO_PATH = Path("assets/images/logo.png")

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

UPLOAD_PAGE_EMPTY_FILE_ERROR_MESSAGE = (
    "The selected file is empty. Please choose a non-empty PDF document."
)
UPLOAD_PAGE_SAVE_ERROR_MESSAGE = (
    "We couldn't save your document. Please try again or choose another PDF."
)

UPLOAD_PAGE_STYLE_PATH = Path("assets/styles/upload.css")

#########################################################################################
# Preprocess Page
#########################################################################################
PREPROCESS_PAGE_SPINNER_MESSAGE = "Processing document..."

PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW = [1, 2, 1]

PREPROCESS_PAGE_PUBGUARD_VERDICT_PASS_KEY = "pass"

PREPROCESS_PAGE_ACADEMIC_VALIDATION_ERROR_MESSAGE = (
    "We couldn't verify that this is a readable academic PDF. "
    "Please upload an academic document and try again."
)
PREPROCESS_PAGE_PDF_CONVERSION_ERROR_MESSAGE = (
    "We couldn't read the content of this PDF. "
    "Please check that the file is valid and try again."
)
PREPROCESS_PAGE_CHUNKING_ERROR_MESSAGE = (
    "We couldn't organize the document content for processing. "
    "Please try another PDF."
)
PREPROCESS_PAGE_INDEXING_ERROR_MESSAGE = (
    "We couldn't prepare the document for search. Please try again."
)

PREPROCESS_PAGE_STYLE_PATH = Path("assets/styles/preprocess.css")

#########################################################################################
# Chat Page
#########################################################################################
CHAT_PAGE_INPUT_PLACEHOLDER = "Ask something about your document..."

CHAT_PAGE_RESET_CONVERSATION_BUTTON_LABEL = "Reset Conversation"
CHAT_PAGE_UPLOAD_NEW_DOCUMENT_BUTTON_LABEL = "Upload New Document"

CHAT_PAGE_SPINNER_MESSAGE = "Generating response..."

CHAT_PAGE_MESSAGE_ROLE_KEY = "role"
CHAT_PAGE_MESSAGE_CONTENT_KEY = "content"

CHAT_PAGE_MESSAGE_ROLE_USER = "user"
CHAT_PAGE_MESSAGE_ROLE_ASSISTANT = "assistant"

CHAT_PAGE_ASSISTANT_AVATAR = "💡"
CHAT_PAGE_USER_AVATAR = "👤"

CHAT_PAGE_STYLE_PATH = Path("assets/styles/chat.css")

CHAT_PAGE_INITIALIZATION_ERROR_MESSAGE = (
    "We couldn't start the chat. Please make sure Ollama is running "
    "and try again."
)
CHAT_PAGE_RESPONSE_GENERATION_ERROR_MESSAGE = (
    "We couldn't generate a response. Please try again."
)

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
