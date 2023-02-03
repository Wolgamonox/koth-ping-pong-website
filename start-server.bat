@echo off

:: Open browser to show QR code
start "" explorer http://127.0.0.1:17809/show-qr

:: Start server
call venv\Scripts\activate.bat
call flask --app server run --host=0.0.0.0 -p 17809

