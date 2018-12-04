from flask import Flask, request, jsonify
from flask_cors import CORS
from lightning import LightningRpc
import os
import random

# Setup flask app object
app = Flask(__name__)
CORS(app)


def default_configdir():
    home = os.getenv("HOME")
    if home:
        return os.path.join(home, ".lightning")
    return "."

# Setup lightning rpc wrapper
rpc_path = os.path.join(default_configdir(), "lightning-rpc")
ld = LightningRpc(rpc_path)


# Generate random labels
def label_generator():
    return 'lbl_{}'.format(random.randint(1, 100000000))


#
# POST /api/generate_invoice
# {
#     "msatoshi": <amount>       (required)
#     "description": <string>    (optional)
#     "expiry": <seconds>        (optional)
# }
#
# Response
# {
#     "payment_hash": <string>
#     "expires_at": <unix timestamp>
#     "bolt11": <bolt11 string>
#     "label": <label_id for payment>
# }
#
@app.route('/api/generate_invoice', methods=['POST'])
def make_invoice():
    data = request.get_json()
    assert 'msatoshi' in data
    amount = data['msatoshi']
    description = data.get('description', '')
    expiry = data.get('expiry', 600)
    label = label_generator()
    try:
        invoice = ld.invoice(amount, label, description, expiry)
        # Add label so you can check status through API
        invoice['label'] = label
        return jsonify(invoice)
    except Exception as e:
        return jsonify({"error": str(e)})


# Check payment status of invoice with <label>
#
# Response
# {
#     "status": "paid|unpaid|expired"
#     "expires_at": <unix_timestamp>
# }
#
@app.route('/api/check_invoice/<label>', methods=['GET'])
def check_invoice(label):
    try:
        data = ld.listinvoices(label)['invoices'][0]
        status = data['status']
        expires = data['expires_at']
        return jsonify({"status": status, "expires_at": expires})
    except IndexError:
        return jsonify({"error": "label does not exist"})


#  Wait for payment on invoice with <label>
#
#  WARNING: May timeout depending on server config
#
@app.route('/api/wait_invoice/<label>', methods=['GET'])
def wait_for_invoice(label):
    try:
        return jsonify(ld.waitinvoice(label))
    except Exception as e:
        return jsonify({"error": str(e)})


# Get node info
@app.route('/api/getinfo')
def getinfo():
    return jsonify(ld.getinfo())

#
# Test API
#
#


# Get a fake bolt invoice
@app.route('/test/generate_invoice', methods=['POST'])
def test_invoice():
    data = request.get_json()
    assert 'msatoshi' in data
    data = {
        "payment_hash": "fake_hash",
        "expires_at": 234132412,
        "bolt11": "asdlfjaljfdlsajfdlsajdflsajdflksajdflasjdflksajdflksajfdlksajasdflkjasdfasdfasdfasdfasdfasdfsadfasdfasdfsadfsadfsadfsadfsadfasdfasdfsadfsadfsadfsadfafffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "label": "fake_label"
    }
    return jsonify(data)


# Check on fake invoice
#
# endpoint will just waits 5 seconds and return
@app.route("/test/check_invoice/<label>", methods=['GET'])
def check_fake_invoice(label):
    import time
    time.sleep(5)
    return jsonify({'status': 'paid'})
