"""src/chat.py"""

import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.llms.ollama import Ollama

from config import config
from const import (
    CHAT_PAGE_ASSISTANT_AVATAR,
    CHAT_PAGE_INPUT_PLACEHOLDER,
    CHAT_PAGE_MESSAGE_CONTENT_KEY,
    CHAT_PAGE_MESSAGE_ROLE_ASSISTANT,
    CHAT_PAGE_MESSAGE_ROLE_KEY,
    CHAT_PAGE_MESSAGE_ROLE_USER,
    CHAT_PAGE_RESET_CONVERSATION_BUTTON_LABEL,
    CHAT_PAGE_SPINNER_MESSAGE,
    CHAT_PAGE_STYLE_PATH,
    CHAT_PAGE_UPLOAD_NEW_DOCUMENT_BUTTON_LABEL,
    CHAT_PAGE_USER_AVATAR,
    LOGO_PATH,
    SESSION_STATE_CHAT_ENGINE_KEY,
    SESSION_STATE_INDEX_KEY,
    SESSION_STATE_MESSAGE_HISTORY_KEY,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
    SYSTEM_PROMPT,
)


def render_chat_page() -> None:
    """Render the chat page for the Streamlit app.

    This function applies custom styling, shows a sidebar with options to reset
    the conversation or upload a new document, initializes the chat engine and
    message history, shows the message history, and handles user input for chatting
    with the assistant.

    Returns:
        None
    """
    # Custom CSS
    with open(CHAT_PAGE_STYLE_PATH) as f:
        css = f.read()

    st.markdown(
        f"""<style>{css}</style>""",
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        # Logo
        st.image(LOGO_PATH)

        # Reset conversation button
        if st.button(
            CHAT_PAGE_RESET_CONVERSATION_BUTTON_LABEL,
            use_container_width=True,
        ):
            st.session_state[SESSION_STATE_MESSAGE_HISTORY_KEY] = []
            st.session_state[SESSION_STATE_CHAT_ENGINE_KEY].reset()
            st.rerun()

        # Upload new document button
        if st.button(
            CHAT_PAGE_UPLOAD_NEW_DOCUMENT_BUTTON_LABEL,
            use_container_width=True,
        ):
            st.session_state[SESSION_STATE_INDEX_KEY] = None
            st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY] = None
            st.session_state[SESSION_STATE_MESSAGE_HISTORY_KEY] = []
            if SESSION_STATE_CHAT_ENGINE_KEY in st.session_state:
                del st.session_state[SESSION_STATE_CHAT_ENGINE_KEY]
            st.rerun()

    # Initialize the chat engine
    if SESSION_STATE_CHAT_ENGINE_KEY not in st.session_state:
        st.session_state[SESSION_STATE_CHAT_ENGINE_KEY] = (
            _initialize_chat_engine(
                st.session_state[SESSION_STATE_INDEX_KEY],
                config.llm_model_name,
                SYSTEM_PROMPT,
                config.chat_mode,
                config.similarity_top_k,
            )
        )

    # Initialize the message history
    if SESSION_STATE_MESSAGE_HISTORY_KEY not in st.session_state:
        st.session_state[SESSION_STATE_MESSAGE_HISTORY_KEY] = []

    # Message history
    for message in st.session_state[SESSION_STATE_MESSAGE_HISTORY_KEY]:
        # Determine the avatar based on the message role
        avatar = (
            CHAT_PAGE_ASSISTANT_AVATAR
            if message[CHAT_PAGE_MESSAGE_ROLE_KEY]
            == CHAT_PAGE_MESSAGE_ROLE_ASSISTANT
            else CHAT_PAGE_USER_AVATAR
        )

        # Message with the appropriate avatar and content
        with st.chat_message(
            message[CHAT_PAGE_MESSAGE_ROLE_KEY],
            avatar=avatar,
        ):
            # Message content
            st.markdown(message[CHAT_PAGE_MESSAGE_CONTENT_KEY])

    # Chat input
    if prompt := st.chat_input(CHAT_PAGE_INPUT_PLACEHOLDER):
        # User message
        st.session_state[SESSION_STATE_MESSAGE_HISTORY_KEY].append(
            {
                CHAT_PAGE_MESSAGE_ROLE_KEY: CHAT_PAGE_MESSAGE_ROLE_USER,
                CHAT_PAGE_MESSAGE_CONTENT_KEY: prompt,
            },
        )
        with st.chat_message(
            CHAT_PAGE_MESSAGE_ROLE_USER,
            avatar=CHAT_PAGE_USER_AVATAR,
        ):
            st.markdown(prompt)

        # Assistant response
        with (
            st.chat_message(
                CHAT_PAGE_MESSAGE_ROLE_ASSISTANT,
                avatar=CHAT_PAGE_ASSISTANT_AVATAR,
            ),
            st.spinner(CHAT_PAGE_SPINNER_MESSAGE),
        ):
            response = st.session_state[SESSION_STATE_CHAT_ENGINE_KEY].chat(
                prompt,
            )
            st.markdown(response.response)

        # Save the assistant response in the message history
        st.session_state[SESSION_STATE_MESSAGE_HISTORY_KEY].append(
            {
                CHAT_PAGE_MESSAGE_ROLE_KEY: CHAT_PAGE_MESSAGE_ROLE_ASSISTANT,
                CHAT_PAGE_MESSAGE_CONTENT_KEY: response.response,
            },
        )


def _initialize_chat_engine(
    index: VectorStoreIndex,
    model: str,
    system_prompt: str,
    chat_mode: str,
    similarity_top_k: int,
) -> BaseChatEngine:
    """Initialize the chat engine.

    This function initializes the chat engine using the provided
    vector store index, LLM model, and chat mode.

    Args:
        index (VectorStoreIndex):
            The vector store index containing document embeddings.
        model (str):
            The name of the LLM model (Ollama) to use for generating responses.
        system_prompt (str):
            The system prompt to guide the behavior of the chat engine.
        chat_mode (str):
            The mode of the chat engine.
        similarity_top_k (int):
            The number of top similar documents to retrieve for context in the chat engine.

    Returns:
        BaseChatEngine: The initialized chat engine.
    """
    llm = Ollama(model=model)
    return index.as_chat_engine(
        chat_mode=chat_mode,
        llm=llm,
        similarity_top_k=similarity_top_k,
        system_prompt=system_prompt,
    )
