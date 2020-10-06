
This is the helper script to update origin DNS servers for secondary DNS service on nic.ru

Follow the doc https://www.nic.ru/help/oauth-server_3642.html to create client_id/client_secret
https://www.nic.ru/manager/oauth.cgi?step=oauth.app_register

source venv/bin/activate
pip install -r requirements.txt

expot NIC_USER=
expot NIC_PASSWORD=
expot NIC_CLIENT_ID=
expot NIC_CLIENT_SECRET=
expot NIC_SERVICE_ID=
nic_password=os.environ['NIC_PASSWORD']
nic_client_id=os.environ['NIC_CLIENT_ID']
nic_client_secret=os.environ['NIC_CLIENT_SECRET']
nic_client_service_id=os.environ['NIC_SERVICE_ID']

./secondary-update-origin.py -d "DOMAIN1, DOMAIN2" -o "DNS1, DNS2"
./secondary-update-origin.py -d "DOMAIN3" -o "DNS3"

deactivate

