#!/bin/bash
cd "$(dirname "$0")"
echo "Starting FilterIQ server..."
echo "Open http://localhost:8000 in your browser"
echo "Press Ctrl+C to stop"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
