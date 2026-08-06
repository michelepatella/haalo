"""src/config.py"""


class Config:
    """Configuration class for the application.

    Attributes:
        chunk_size (int):
            The size of the chunks to be used for document processing.
        chunk_overlap (int):
            The overlap size of the chunks to be used for document processing.
        embedding_model_name (str):
            The name of the embedding model to be used.
        llm_model_name (str):
            The name of the LLM model to be used.
        chat_mode (str):
            The chat mode to be used in the chat engine.
    """

    def __init__(self) -> None:
        """Initialize the configuration object.

        Returns:
            None
        """
        self.chunk_size: int = 512
        self.chunk_overlap: int = 50
        self.embedding_model_name: str = "BAAI/bge-small-en-v1.5"
        self.llm_model_name: str = "qwen2.5:3b"
        self.chat_mode: str = "condense_question"


config = Config()
