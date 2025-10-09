#!/bin/bash
# Start the backend with environment variables from .env

# Load .env file and export variables
set -a
source ../.env
set +a

# Start the server
./venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
