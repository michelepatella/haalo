.PHONY: run

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
