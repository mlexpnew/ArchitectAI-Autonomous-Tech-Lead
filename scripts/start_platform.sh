#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "🚀 Launching ArchitectAI Multi-Agent Platform"
echo "=========================================================="

echo "Starting ArchitectAI FastAPI REST API Engine on port 8000..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

echo "Starting ArchitectAI Streamlit Web Platform on port 8501..."
python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
STREAMLIT_PID=$!

echo "✅ Both services running:"
echo "   - FastAPI Swagger Docs: http://localhost:8000/docs"
echo "   - Streamlit Web UI:     http://localhost:8501"

trap "kill -TERM $FASTAPI_PID $STREAMLIT_PID" SIGTERM SIGINT

wait -n $FASTAPI_PID $STREAMLIT_PID
