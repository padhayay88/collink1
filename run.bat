@echo off

TITLE Collink Backend
START cmd /c "python main.py"

TITLE Collink Frontend
REM Ensure API URL is set for the frontend in this session
START cmd /c "cd frontend && set NEXT_PUBLIC_API_URL=http://localhost:8000 && npm run dev"
