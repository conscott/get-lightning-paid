from flask import Flask, request, jsonify
from lightning import LightningRpc
import os
import random

# Setup flask app object
app = Flask(__name__)


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
    expiry = data.get('expiry', 3600)
    label = label_generator()
    invoice = ld.invoice(amount, label, description, expiry)
    # Add label so you can check status through API
    invoice['label'] = label
    return jsonify(invoice)


# Check payment status of invoice with <label>
#
# Response
# {
#     "status": "paid|unpaid|expired"
# }
#
@app.route('/api/check_invoice/<label>', methods=['GET'])
def check_invoice(label):
    try:
        status = ld.listinvoices(label)['invoices'][0]['status']
        print("Status: %s" % status)
        return jsonify({"status": status})
    except IndexError:
        return jsonify({"error": "label does not exist"})


#  Wait for payment on invoice with <label>
#
#  WARNING: May timeout depending on server config
#
@app.route('/api/wait_invoice/<label>', methods=['GET'])
def wait_for_invoice(label):
    return jsonify(ld.waitinvoice(label))


# List all invoices
@app.route('/api/list_invoices', methods=['GET'])
def list_invoices():
    return jsonify(ld.listinvoices())


# Get node info
@app.route('/api/getinfo')
def getinfo():
    return jsonify(ld.getinfo())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
