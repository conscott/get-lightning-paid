## Description

A simple Flask REST API to generate lightning invoices and wait for payment confirmation / check invoice status. The application server should not be exposed to the public internet, as it would allow anyone to generate invoices on your lightning node. 

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
