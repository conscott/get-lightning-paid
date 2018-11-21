## Description

A simple Flask REST API to generate lightning invoices and wait for payment confirmation / check invoice status. This is experimential fun and not enterprise ready. *Use with caution!*

### Files
* API implementation in [app.py](./app.py) 
* Sample usage in script [gen_invoice_and_pay.py](./gen_invoice_and_pay.py)

The app requires a locally running version of [c-lightning](https://github.com/ElementsProject/lightning)

### Install Environment
```
sudo apt-get install python3-dev
python3 -v venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Server

For development/test server
```
./run_dev.sh
```

For production server using uWSGI
```
./run_prod.sh
```
You can tweak uwsgi configuration in [uwsgi.ini](./uwsgi.ini)

## API

### Generate Invoice


#### POST /api/generate_invoice
```
{
    "msatoshi": <amount>       (required)
    "description": <string>    (optional, defatul '')
    "expiry": <seconds>        (optional, default 600)
}
```

#### Response
```
{
    "payment_hash": <string>
    "expires_at": <unix timestamp>
    "bolt11": <bolt11 string>
    "label": <string label_id for payment>
}
```

Note the `label` is needed to check invoice status later

### Check Invoice

#### GET /api/check_invoice/\<label\>
Check the status of the invoice with the given `label`

#### Response
```
{
    "status": "paid|unpaid|expired"
    "expires_at": <unix timesamp>
}
```

### Wait For Invoice Payment

#### GET /api/wait_invoice/\<label\>

Will wait until the invoice associated with the label has been paid

#### Response
```
{
  "label": <string>
  "bolt11": <string>
  "payment_hash": <string>
  "msatoshi": <int>
  "status": "paid", 
  "pay_index": <int>
  "msatoshi_received": <int>
  "paid_at": <unix timestamp>
  "description": <string>
  "expires_at": <unix timesamp>
}
```


### Try it out

Check out the script [gen_invoice_and_pay.py](./gen_invoice_and_pay.py) to see a sample backend flow
