@echo off

:: Python requirements installation
echo Checking Python environment ...
if exist venv\ (
    cls
    echo Checking Python environment ... Found
    call venv\Scripts\activate.bat
) else (
    echo No environment found, creating virtual environment venv ...
    python -m virtualenv venv && venv\Scripts\activate.bat && pip install -r requirements.txt
    cls
    echo No environment found, creating virtual environment venv ... Done
)

:: Open browser to show QR code
explorer http://127.0.0.1:17809/show-qr

:: Start server
call flask --app server run --host=0.0.0.0 -p 17809

