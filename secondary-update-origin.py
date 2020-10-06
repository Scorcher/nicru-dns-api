#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

def enable_debug():
    import logging

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


#================
# API DOC
# https://www.nic.ru/help/upload/file/API_DNS-hosting.pdf
# https://www.nic.ru/help/oauth-server_3642.html
#================

api_url='https://api.nic.ru'
token_url='https://api.nic.ru/oauth/token'
token_scope=["(GET|POST):/dns-master/.+"]
nic_user=os.environ['NIC_USER']
nic_password=os.environ['NIC_PASSWORD']
nic_client_id=os.environ['NIC_CLIENT_ID']
nic_client_secret=os.environ['NIC_CLIENT_SECRET']
nic_client_service_id=os.environ['NIC_SERVICE_ID']


def get_oauth_session(user, password, client_id, client_secret, token_url, token_scope):
    
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id, scope=token_scope), scope=token_scope)
    oauth.fetch_token(token_url=token_url,
        username=user, password=password,
        client_id=client_id, client_secret=client_secret, scope=token_scope)

    return oauth


def update_origin(domain, origin):
    
    client = get_oauth_session(nic_user, nic_password, nic_client_id, nic_client_secret, token_url, token_scope)

    domains = domain.split(",")
    origins = origin.split(",")

    root = Element('request')
    for o in origins:
        o = o.strip()
        child = SubElement(root, 'address')
        child.text = o

    body = tostring(root, encoding="UTF-8")

    for d in domains:
        d = d.strip()
        url = api_url + '/dns-master/services/' + nic_client_service_id + '/zones/' + d + '/masters'
        response = client.post(url, data=body).content
        root = ET.fromstring(response)
        status = root.find('status')
        if 'success' != status.text:
            print("Domain " + d + ' set ' + origin + ': error (' + status.text + ')')
            continue

        print("Domain " + d + ' set ' + origin + ': OK')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='domain', help='Domain names in punycode format, delimeted by ","',
                        required=True, type=str)
    parser.add_argument('-o', dest='origin', help='Origin servers IP addresses, delimeted by ","',
                        required=True, type=str)

    args = parser.parse_args()

    #enable_debug()
    update_origin(args.domain, args.origin)

    exit(0)
