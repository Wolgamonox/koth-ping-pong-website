from flask import Flask
from flask import request
from flask import render_template
from flask_qrcode import QRcode

from datetime import datetime
import netifaces
import json
import pandas as pd

import os  
os.makedirs('games_data', exist_ok=True) 


app = Flask(__name__)
qrcode = QRcode(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/show-qr")
def show_qr():
    
    # To get host ip
    for iface in netifaces.interfaces():
        iface_details = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in iface_details:
            for ip_interfaces in iface_details[netifaces.AF_INET]:
                for key, ip_add in ip_interfaces.items():
                    if key == 'addr' and ip_add != '127.0.0.1' and not ip_add.startswith('172'):
                        host_ip = ip_add


    host_name = '%s:%d' % (host_ip, 17809)
    return render_template('qr_code.html', host_name=host_name)


@app.route('/upload', methods=['POST'])
def upload():
    parse_json_to_csv(request.data.decode())

    return "Success", 200


def parse_json_to_csv(raw_json):
    now = datetime.now().strftime("%d.%m.%Y %H_%M_%S")
    filename = 'games_data/game (%s).csv' % now

    print(filename)
    
    transitions = json.loads(raw_json)['transitions']
    df = pd.DataFrame({
        'Name': [list(transition.keys())[0] for transition in transitions],
        'Interval': [list(transition.values())[0] for transition in transitions]
    })

    print(df)
    df.to_csv(filename)
