.PHONY: run
.PHONY: benchmark-preprocessing

export PYTHONPATH := .:${CURDIR}/src

MODEL := $(shell PYTHONPATH=. python -c "from src.config import config; print(config.llm_model_name)")

run:
	@bash -c '\
		echo "🚀 Starting Ollama background service..."; \
		ollama serve > /dev/null 2>&1 & OLLAMA_PID=$$!; \
		trap "echo -e \"\n🧹 Stopping Ollama service...\"; kill $$OLLAMA_PID 2>/dev/null" INT TERM EXIT; \
		sleep 2; \
		echo "🔍 Checking for model $(MODEL)..."; \
		ollama list | grep -q "$(MODEL)" || ollama pull $(MODEL); \
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
