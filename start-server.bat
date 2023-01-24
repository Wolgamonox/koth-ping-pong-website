call venv\Scripts\activate.bat
pip install -r requirements.txt -q
explorer http://127.0.0.1:17809/show-qr
flask --app server run --host=0.0.0.0 -p 17809