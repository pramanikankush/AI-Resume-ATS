#!/bin/bash

# Start FastAPI backend in the background
echo "Starting FastAPI backend on port 8000..."
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 &

# Start Streamlit frontend in the foreground
echo "Starting Streamlit frontend on port $PORT..."
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
