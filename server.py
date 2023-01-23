from summary_creator import *

from flask import Flask, request, render_template, redirect, url_for
from flask_qrcode import QRcode

from datetime import datetime
import netifaces
import json
import pandas as pd

import webbrowser
import io

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import os

os.makedirs('games_data', exist_ok=True)

app = Flask(__name__)
qrcode = QRcode(app)


@app.route("/show-qr")
def show_qr():
    host_name = get_hostname()
    return render_template('qr_code.html', host_name=host_name)


@app.route('/summary')
def summary():
    return render_template('game_summary.html', filename=request.args['filename'])


@app.route('/plot_summary.png')
def plot_summary():
    summary_filename = request.args.get('filename')
    fig = generate_summary(summary_filename)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/upload', methods=['POST'])
def upload():
    now = datetime.now().strftime("%d-%m-%Y %H_%M_%S")
    filename = 'games_data/game (%s).csv' % now

    print(filename)
    parse_json_to_csv(filename, request.data.decode())

    save_summary(filename)

    webbrowser.open('http://' + get_hostname() + url_for('plot_summary', filename=filename))

    return 'Success', 200


def parse_json_to_csv(filename, raw_json):
    transitions = json.loads(raw_json)['transitions']
    df = pd.DataFrame({
        'Name': [list(transition.keys())[0] for transition in transitions],
        'Interval': [list(transition.values())[0] for transition in transitions]
    })

    print(df)
    df.to_csv(filename)


def get_hostname():
    # To get host ip
    for iface in netifaces.interfaces():
        iface_details = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in iface_details:
            for ip_interfaces in iface_details[netifaces.AF_INET]:
                for key, ip_add in ip_interfaces.items():
                    # filter localhost and WSL interface
                    if key == 'addr' and ip_add != '127.0.0.1' and not ip_add.startswith('172'):
                        host_ip = ip_add

    return '%s:%d' % (host_ip, 17809)
