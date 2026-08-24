<br/>
<div align="center">
    <img width="50%" src="https://github.com/user-attachments/assets/70faf79b-7b84-4450-9a87-abbc2476a07f"/> <br>
    <em>Multi-turn RAG chatbot for conversational analysis of academic documents.</em>
  </p>

  [![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
  [![LlamaIndex](https://img.shields.io/badge/LlamaIndex-2E00F7?style=for-the-badge&logo=llama&logoColor=white)](https://www.llamaindex.ai/)
  [![ChromaDB](https://img.shields.io/badge/ChromaDB-ED6E51?style=for-the-badge&logo=chroma&logoColor=white)](https://www.trychroma.com/products/chromadb)
  [![Ollama](https://img.shields.io/badge/Ollama-FFFFFF?style=for-the-badge&logo=ollama&logoColor=black)](https://ollama.com/)
  [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
</div>

---

## About The Project

https://github.com/user-attachments/assets/95e59c32-7bc3-471b-8e09-df08de1f47f1

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


## License

Distributed under the [MIT License](https://github.com/michelepatella/haalo/blob/main/LICENSE).

---

<div align="center">
  <sub>Haalo is powered by AI. It can make mistakes, so please verify important information.</sub>
</div>
