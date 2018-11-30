virtualenv env
source env/bin/activate
pip install -r requirements.txt
python cart.py --project_id=smart-cart-uf --registry_id=shop1 --device_id=cart1 --private_key_file=/home/pi/Documents/rsa_private.pem --algorithm=RS256
