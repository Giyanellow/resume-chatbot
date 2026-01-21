#!/bin/bash
set -e

echo "Starting Ollama service..."
/bin/ollama serve &

echo "Waiting for Ollama to be ready..."
sleep 5

echo "Pulling model: ${MODEL_NAME:-granite3.1-moe:1b}"
ollama pull "${MODEL_NAME:-granite3.1-moe:1b}"

echo "Ollama initialization complete!"
wait
