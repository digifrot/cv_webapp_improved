@echo off
cd /d "C:\Projects\cv_webapp_improved"

REM Activate virtual environment
call venv\Scripts\activate

REM Open browser automatically
start "" http://127.0.0.1:5000/

REM Start the Flask app
python app.py

pause
