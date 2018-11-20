#!/usr/bin/env python3

#
# Need dev server running on localhost:5000
#
# Generate invoice and wait for payment
#

import requests

# Point to running flask app
host = 'http://localhost:5000'

# POST to make an invoice
data = {'msatoshi': 12000, 'description': 'test invoice'}
r = requests.post(host + '/api/generate_invoice', json=data)
assert r.status_code == 200
invoice_data = r.json()
print("Generated invoice:\n\n%s\n" % invoice_data['bolt11'])

# Now have to externally pay the invoice while endpoint waits
# for payment confirmation
print("Waiting for payment....")
r = requests.get(host + "/api/wait_invoice/%s" % invoice_data['label'])
assert r.status_code == 200

print("Paid!")
