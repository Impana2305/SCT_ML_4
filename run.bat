@echo off
echo Starting Backend...
start cmd /k "python app.py"

echo Starting Frontend...
cd frontend
start cmd /k "npm run dev"

echo Both servers are starting in separate windows.
