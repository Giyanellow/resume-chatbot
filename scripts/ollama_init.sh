#!/bin/bash
/bin/ollama serve &

sleep 5

ollama pull granite3.1-moe:1b

wait
EOF
