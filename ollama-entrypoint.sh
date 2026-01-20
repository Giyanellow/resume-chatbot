#!/bin/bash

# Start Ollama in the background
/bin/ollama serve &

# Wait for Ollama to be ready
sleep 5

# Pull the model
ollama pull granite3.1-moe:1b

# Keep the container running
wait
