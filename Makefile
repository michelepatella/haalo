.PHONY: run
.PHONY: benchmark-preprocessing

export PYTHONPATH := .:${CURDIR}/src

LLM_MODEL_NAME := $(shell PYTHONPATH=. python -c "from src.config import config; print(config.llm_model_name)")
PUBGUARD_MODELS_LOCAL_DIR := $(HOME)/.pubguard/models
PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_NAME := head_doc_type.npz
PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_LOCAL_PATH := $(PUBGUARD_MODELS_LOCAL_DIR)/$(PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_NAME)
PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_DOWNLOAD_URL := https://huggingface.co/jimnoneill/pub-guard/resolve/main/models/$(PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_NAME)?download=true

run:
	@bash -c '\
		echo "🚀 Starting Ollama background service..."; \
		ollama serve > /dev/null 2>&1 & OLLAMA_PID=$$!; \
		trap "echo -e \"\n🧹 Stopping Ollama service...\"; kill $$OLLAMA_PID 2>/dev/null" INT TERM EXIT; \
		sleep 2; \
		echo "🔍 Checking for model $(LLM_MODEL_NAME)..."; \
		ollama list | grep -q "$(LLM_MODEL_NAME)" || ollama pull $(LLM_MODEL_NAME); \
		echo "🔍 Checking for the PubGuard document-type classifier..."; \
		if [ ! -s "$(PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_LOCAL_PATH)" ]; then \
			mkdir -p "$(PUBGUARD_MODELS_LOCAL_DIR)"; \
			curl --fail --location --silent --show-error \
				"$(PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_DOWNLOAD_URL)" \
				--output "$(PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_LOCAL_PATH)"; \
			echo "PubGuard model installed in $(PUBGUARD_DOCUMENT_TYPE_CLASSIFIER_LOCAL_PATH)"; \
		fi; \
		echo "💡 Launching Haalo..."; \
		streamlit run src/app.py; \
	'

benchmark-preprocessing:
	@PYTHONPATH=.:src \
	HF_HUB_DISABLE_SYMLINKS_WARNING=1 \
	HF_HUB_DISABLE_IMPLICIT_TOKEN_WARNING=1 \
	HF_HUB_ENABLE_HF_TRANSFER=0 \
	HF_HUB_VERBOSITY=error \
	TRANSFORMERS_VERBOSITY=error \
	TQDM_DISABLE=1 \
	PYTHONWARNINGS="ignore" \
	python benchmarks/preprocessing/run_benchmark.py
