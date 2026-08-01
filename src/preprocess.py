"""src/preprocess.py"""

import chromadb
import pymupdf4llm
import streamlit as st
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import BaseNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from const import (
    EMBEDDING_MODEL_NAME,
    PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW,
    PREPROCESS_PAGE_SPINNER_MESSAGE,
    PREPROCESS_PAGE_STYLE_PATH,
    SESSION_STATE_INDEX_KEY,
    VECTOR_STORE_COLLECTION_NAME,
    VECTOR_STORE_PERSIST_DIR,
)


def render_preprocess_page(uploaded_doc_path: str) -> None:
    """Render the preprocess page for the Streamlit app.

    This function applies custom CSS styling to the preprocess page
    and runs the preprocess pipeline on the uploaded document.

    Args:
        uploaded_doc_path (str):
            The absolute path to the uploaded document.

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

    # Run preprocess pipeline and save the resulting
    # index in session state
    _, col_content, _ = st.columns(PREPROCESS_PAGE_COLUMN_LAYOUT_NARROW)
    with col_content, st.spinner(PREPROCESS_PAGE_SPINNER_MESSAGE):
        index = _run_preprocess_pipeline(uploaded_doc_path)
        if index is not None:
            st.session_state[SESSION_STATE_INDEX_KEY] = index


def _pdf_to_md(pdf_path: str) -> str:
    """Converts a PDF document to Markdown.

    This function converts a PDF document to Markdown using
    the pymupdf4llm library.

    Args:
        pdf_path (str):
            The absolute path to the PDF document.

    Returns:
        str:
            The Markdown content extracted from the PDF document.
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text


def _chunk_md(md_text: str) -> list[dict]:
    """Splits Markdown text into chunks.

    This function takes Markdown text and splits it into chunks
    based on the document structure.

    Args:
        md_text (str):
            The Markdown text to be chunked.

    Returns:
        list[dict]:
            List of chunks.
    """
    # Create a Document object from the Markdown text
    doc = Document(text=md_text)

    # Use the MarkdownNodeParser to split the
    # document into nodes (chunks)
    parser = MarkdownNodeParser()

    # Get nodes (chunks) from the document and return them
    nodes = parser.get_nodes_from_documents([doc])
    return nodes


def _create_and_store_embeddings(
    nodes: list[BaseNode],
    embed_model_name: str,
    collection_name: str,
    persist_dir: str,
) -> VectorStoreIndex:
    """Creates embeddings for the given nodes and stores them in a vector database.

    This function initializes an embedding model, creates a persistent ChromaDB client,
    and stores the embeddings of the given nodes in a ChromaDB collection.

    Args:
        nodes (list[BaseNode]):
            List of nodes (chunks) for which embeddings will be created.
        embed_model_name (str):
            The name of the embedding model to be used for creating embeddings.
        collection_name (str):
            The name of the ChromaDB collection to store the embeddings.
        persist_dir (str):
            The directory where the ChromaDB database will be persisted.

    Returns:
        VectorStoreIndex:
            The resulting vector database instance.
    """
    # Initialize the embedding model
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)

    # Initialize a persistent ChromaDB client
    db_client = chromadb.PersistentClient(path=persist_dir)

    # Create or get the ChromaDB collection
    chroma_collection = db_client.get_or_create_collection(
        name=collection_name,
    )

    # Create a ChromaVectorStore using the collection
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Create a StorageContext using the vector store
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create a VectorStoreIndex using the nodes, storage context, and embedding model
    # and return it
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    return index


def _run_preprocess_pipeline(uploaded_doc_path: str) -> VectorStoreIndex:
    """Executes the complete preprocess pipeline.

    This function orchestrates the entire preprocess pipeline:
    1. Converts the PDF document to Markdown
    2. Chunks the Markdown document into sections
    3. Computes embeddings for each chunk
    4. Stores the embeddings in a vector database

    Args:
        uploaded_doc_path (str):
            The absolute path to the uploaded document.

    Returns:
        VectorStoreIndex:
            The resulting vector database instance.
    """
    # 1. Converts the PDF document to Markdown
    md_content = _pdf_to_md(uploaded_doc_path)

    # 2. Chunks the Markdown document into sections
    chunks = _chunk_md(md_content)

    # 3. Computes embeddings for each chunk &
    # 4. Stores the embeddings in a vector database
    index = _create_and_store_embeddings(
        chunks,
        EMBEDDING_MODEL_NAME,
        VECTOR_STORE_COLLECTION_NAME,
        VECTOR_STORE_PERSIST_DIR,
    )

    return index
