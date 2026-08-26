<br/>
<div align="center">
    <img width="50%" src="https://github.com/user-attachments/assets/70faf79b-7b84-4450-9a87-abbc2476a07f"/> <br>
    
  [![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
  [![LlamaIndex](https://img.shields.io/badge/LlamaIndex-2E00F7?style=for-the-badge&logo=llama&logoColor=white)](https://www.llamaindex.ai/)
  [![ChromaDB](https://img.shields.io/badge/ChromaDB-ED6E51?style=for-the-badge&logo=chroma&logoColor=white)](https://www.trychroma.com/products/chromadb)
  [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
  [![Ollama](https://img.shields.io/badge/Ollama-FFFFFF?style=for-the-badge&logo=ollama&logoColor=black)](https://ollama.com/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
</div>

<br>

<p><strong>Table of Contents</strong></p>

- [Overview](#overview)
- [RAG Pipeline](#rag-pipeline)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Run](#run)
- [License](#license)

---

## Overview

💡 **Haalo** is a multi-turn RAG chatbot designed for conversational analysis of academic documents, allowing users to ask questions about uploaded files and receive answers grounded exclusively in their content.

https://github.com/user-attachments/assets/95e59c32-7bc3-471b-8e09-df08de1f47f1

## RAG Pipeline

**`1 • Document Upload`**  
Users upload an academic document in PDF format.  
**↓**  
**`2 • Document Preprocessing`**  
The uploaded document undergoes a multi-stage preprocessing pipeline:  

> **`2.1 • PDF to Markdown Conversion`**  
> The PDF is converted to Markdown to preserve semantic structure and accurately extract content.
>
> **`2.2 • Structure-Aware Chunking`**  
> The Markdown content is first split by document sections, then divided into token-bounded chunks.
>
> **`2.3 • Embedding & Vector Indexing`**  
> Each chunk is converted into an embedding and stored in a ChromaDB vector store for similarity search.

**↓**  
**`3 • Conversational Retrieval & Generation`**  
For each user query, the top-k most relevant document chunks are retrieved from ChromaDB based on semantic similarity and used by a locally hosted LLM to generate document-grounded responses in a multi-turn conversation.

> [!TIP]
> Customize the RAG pipeline by modifying the following parameters in `src/config.py`:
>
> | Parameter              | Default                  |
> | ---------------------- | ------------------------ |
> | `chunk_size`           | `1024`                   |
> | `chunk_overlap`        | `150`                    |
> | `embedding_model_name` | `BAAI/bge-small-en-v1.5` |
> | `llm_model_name`       | `qwen2.5:3b`             |
> | `chat_mode`            | `condense_plus_context`  |
> | `similarity_top_k`     | `5`                      |

## Getting Started

### Prerequisites

**Python**  
Required version: 3.14.6  
Link: https://www.python.org/downloads/release/python-3146/

> [!WARNING]
> Compatibility with earlier or later Python versions has not been tested.

**Git**  
Required to clone the repository.  
Link: https://git-scm.com/install/  

**Ollama**  
Required to run the local LLM.  
Link: https://ollama.com/download

**Make**  
Required to run the application using the provided `Makefile`.

### Installation

Clone the repository from GitHub and install the required dependencies:

```sh
git clone https://github.com/michelepatella/haalo.git
cd haalo
pip install -e .
```

### Run

After installation, run the application locally:

```sh
make run
```

This command starts the Ollama service, downloads the configured LLM if needed, and launches the Streamlit application.

## License

Distributed under the [MIT License](https://github.com/michelepatella/haalo/blob/main/LICENSE).

---

<div align="center">
  <sub>💡 Haalo is powered by AI. It can make mistakes, so please verify important information.</sub>
</div>
