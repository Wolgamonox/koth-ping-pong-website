from flask import Flask, request, render_template, url_for
from flask_qrcode import QRcode
from flask import Response

from datetime import datetime
import netifaces
import webbrowser
import io

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import os

from koth_stats.figures_creator import generate_fig_summary


os.makedirs('games_data', exist_ok=True)

PORT = 17809

app = Flask(__name__)
qrcode = QRcode(app)


###################
#   Flask Views   #
###################

@app.route('/ping')
def ping():
    return "pong", 200


@app.route("/show-qr")
def show_qr():
    """
    Show QR code with address of the server.
    """
    if request.host.split(':')[0] == '127.0.0.1':
        host_name = get_hostname()
        return render_template('qr_code.html', host_name=host_name)
    else:
        return "Ressource only accessible from localhost", 403


@app.route('/summary')
def summary():
    """
    View of summary of a game.
    """
    return render_template('game_summary.html', filename=request.args['filename'])


@app.route('/plot_summary.png')
def plot_summary():
    """
    Renders the summary to a png.
    """
    summary_filename = request.args.get('filename')
    fig_bytes = generate_fig_summary(summary_filename, as_bytes=True)
    return Response(fig_bytes, mimetype='image/png')


@app.route('/upload', methods=['POST'])
def upload(open_browser=True):
    """
    API endpoint for uploading raw app data.
    """
    filename = generate_filename()

    print('Saving to %s.' % filename)
    save_json(filename, request.data.decode())

    if open_browser:
        webbrowser.open('http://' + get_hostname() +
                        url_for('plot_summary', filename=filename))

    return 'Success', 200


def save_json(filename, raw_json):
    """
    Save raw json data to a file.
    """
    with open(filename, 'w') as outfile:
        outfile.write(raw_json)


def generate_filename():
    """
    Generate summary filename based on current datetime.
    """
    now = datetime.now().strftime("%d-%m-%Y %H_%M_%S")
    return 'games_data/game (%s).json' % now


def get_hostname():
    """
    Get hostname of current machine. Filters out local hostname and WSL host.
    """
    for iface in netifaces.interfaces():
        iface_details = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in iface_details:
            for ip_interfaces in iface_details[netifaces.AF_INET]:
                for key, ip_add in ip_interfaces.items():
                    # filter localhost and WSL interface
                    if key == 'addr' and ip_add != '127.0.0.1' and not ip_add.startswith('172'):
                        host_ip = ip_add

    return '%s:%d' % (host_ip, PORT)
