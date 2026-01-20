#!/bin/bash

/bin/ollama serve &

sleep 5

ollama pull "${OLLAMA_MODEL:-granite3.1-moe:1b}"

wait
EOF
