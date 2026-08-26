"""src/preprocess.py"""

import os

import chromadb
import pymupdf4llm
import streamlit as st
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from llama_index.core.schema import BaseNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from config import config
from const import (
    PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW,
    PREPROCESS_PAGE_ERROR_MESSAGE,
    PREPROCESS_PAGE_SPINNER_MESSAGE,
    PREPROCESS_PAGE_STYLE_PATH,
    SESSION_STATE_INDEX_KEY,
    SESSION_STATE_UPLOADED_DOC_PATH_KEY,
    VECTOR_STORE_COLLECTION_NAME,
)


@st.cache_resource
def _get_embedding_model(embedding_model_name: str) -> HuggingFaceEmbedding:
    """Get the embedding model.

    This function initializes and returns a HuggingFaceEmbedding model
    based on the provided model name.

    Args:
        embedding_model_name (str):
            The name of the embedding model to be used.

    Returns:
        HuggingFaceEmbedding:
            The initialized HuggingFaceEmbedding model instance.
    """
    return HuggingFaceEmbedding(model_name=embedding_model_name)


@st.cache_resource
def _get_chroma_client() -> chromadb.Client:
    """Get the ChromaDB client.

    This function initializes and returns a ChromaDB client instance.

    Returns:
        chromadb.Client:
            The initialized ChromaDB client instance.
    """
    return chromadb.Client()


def render_preprocess_page() -> None:
    """Render the preprocess page for the Streamlit app.

    This function applies custom CSS styling to the preprocess page
    and runs the preprocess pipeline on the uploaded document.

    Returns:
        None
    """
    # Custom CSS
    with open(PREPROCESS_PAGE_STYLE_PATH) as f:
        css = f.read()

    st.markdown(
        f"""<style>{css}</style>""",
        unsafe_allow_html=True,
    )

    _, col_content, _ = st.columns(PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW)
    uploaded_doc_path = st.session_state[SESSION_STATE_UPLOADED_DOC_PATH_KEY]
    with col_content, st.spinner(PREPROCESS_PAGE_SPINNER_MESSAGE):
        try:
            # Run preprocess pipeline and save the resulting
            # index in session state
            index = _run_preprocess_pipeline(
                uploaded_doc_path,
                config.chunk_size,
                config.chunk_overlap,
                config.embedding_model_name,
                VECTOR_STORE_COLLECTION_NAME,
            )
            if index is not None:
                st.session_state[SESSION_STATE_INDEX_KEY] = index
                st.rerun()
            else:
                st.error(PREPROCESS_PAGE_ERROR_MESSAGE)
        finally:
            # Clean up the uploaded document
            if os.path.exists(uploaded_doc_path):
                os.remove(uploaded_doc_path)


def _pdf_to_md(pdf_path: str) -> str | None:
    """Convert a PDF document to Markdown.

    This function converts a PDF document to Markdown using
    the pymupdf4llm library.

    Args:
        pdf_path (str):
            The absolute path to the PDF document.

    Returns:
        str | None:
            The Markdown content extracted from the PDF document,
            or None if failed.
    """
    try:
        return pymupdf4llm.to_markdown(pdf_path)
    except Exception:
        return None


def _chunk_md(
    md_text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[BaseNode] | None:
    """Split Markdown text into chunks.

    This function takes Markdown text and splits it into nodes (chunks)
    based on the document structure and token limits.

    Args:
        md_text (str):
            The Markdown text to be chunked.
        chunk_size (int):
            The size of the chunks to be used for document processing.
        chunk_overlap (int):
            The overlap size of the chunks to be used for document processing.

    Returns:
        list[BaseNode] | None:
            List of nodes (chunks), or None if chunking failed.
    """
    try:
        # Create a Document object from the Markdown text
        doc = Document(text=md_text)

        # Use the MarkdownNodeParser to split the
        # document into nodes (chunks) by section
        md_parser = MarkdownNodeParser()
        section_nodes = md_parser.get_nodes_from_documents([doc])

        # Sub-divide section nodes into token-bounded chunks
        # and return them
        sentence_splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        nodes = sentence_splitter.get_nodes_from_documents(section_nodes)
        return nodes
    except Exception:
        return None


def _create_and_store_embeddings(
    nodes: list[BaseNode],
    embedding_model_name: str,
    collection_name: str,
) -> VectorStoreIndex | None:
    """Create embeddings for the given nodes and store them in a vector database.

    This function initializes an embedding model, creates a ChromaDB client,
    and stores the embeddings of the given nodes in a ChromaDB collection.

    Args:
        nodes (list[BaseNode]):
            List of nodes (chunks) for which embeddings will be created.
        embedding_model_name (str):
            The name of the embedding model to be used.
        collection_name (str):
            The name of the ChromaDB collection.

    Returns:
        VectorStoreIndex | None:
            The resulting vector database instance, or None if failed.
    """
    try:
        # Initialize the embedding model
        embedding_model = _get_embedding_model(embedding_model_name)

        # Initialize a ChromaDB client
        db_client = _get_chroma_client()

        # Delete the collection if it already exists
        try:
            db_client.delete_collection(name=collection_name)
        except Exception:
            pass

        # Create or get the ChromaDB collection
        chroma_collection = db_client.get_or_create_collection(
            name=collection_name,
        )

        # Create a ChromaVectorStore using the collection
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # Create a StorageContext using the vector store
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
        )

        # Create a VectorStoreIndex using the nodes, storage context, and
        # embedding model and return it
        return VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            embed_model=embedding_model,
        )
    except Exception:
        return None


def _run_preprocess_pipeline(
    uploaded_doc_path: str,
    chunk_size: int,
    chunk_overlap: int,
    embedding_model_name: str,
    collection_name: str,
) -> VectorStoreIndex | None:
    """Execute the complete preprocess pipeline.

    This function orchestrates the entire preprocess pipeline:
    1. Convert the PDF document to Markdown
    2. Chunk the Markdown document into sections
    3. Compute embeddings for each chunk
    4. Store the embeddings in a vector database

    Args:
        uploaded_doc_path (str):
            The absolute path to the uploaded document.
        chunk_size (int):
            The size of the chunks to be used for document processing.
        chunk_overlap (int):
            The overlap size of the chunks to be used for document processing.
        embedding_model_name (str):
            The name of the embedding model to be used.
        collection_name (str):
            The name of the vector store collection.

    Returns:
        VectorStoreIndex | None:
            The resulting vector database instance, or None if any step fails.
    """
    # 1. Convert the PDF document to Markdown
    md_content = _pdf_to_md(uploaded_doc_path)
    if md_content is None:
        return None

    # 2. Chunk the Markdown document into sections
    chunks = _chunk_md(md_content, chunk_size, chunk_overlap)
    if chunks is None:
        return None

    # 3. Compute embeddings for each chunk &
    # 4. Store the embeddings in a vector database
    return _create_and_store_embeddings(
        chunks,
        embedding_model_name,
        collection_name,
    )
