:: Python requirements installation
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

:: Start server
start "Server" flask --app server run --host=0.0.0.0 -p 17809

:: Open browser to show QR code
start "" explorer http://127.0.0.1:17809/show-qr
