import json
import http.client
import os
import mimetypes
import time
import urllib.parse
import urllib

import requests
from requests.utils import quote

def authenticate():
    uri_path = '/oauth/token'
    hostname = 'fileittax.sharefile.com'
    client_id = "JY9pWeQTOq094sfkuaY6PfdAdVucTGMK"
    client_secret = "mqwUGGBF5qmLgbQ67kFj17m22op2eki5dPKD6ni4IfoWLAX0"
    username = "hero@fileit.tax"
    password = "%*$*yano^OungM!*cH27"

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'password', 'client_id': client_id, 'client_secret': client_secret,
              'username': username, 'password': password}

    response = requests.request("POST", 'https://{}{}'.format(hostname, uri_path), headers=headers, data=params)
    token = None
    if response.status_code == 200:
        token = response.json()['access_token']
        print(token)
    else:
        raise Exception('Unable to authenticate')
    return token


def get_authorization_header(token):
    return {'Authorization': 'Bearer %s' % (token['access_token'])}


def get_hostname(token):
    return '{}.sf-api.com'.format(token['subdomain'])

def get_root(token, get_children=False):
    client_id = "JY9pWeQTOq094sfkuaY6PfdAdVucTGMK"
    root_folder_path = '/Folders/Personal Folders/Clients'
    uri_path = '/sf/v3/Items(allshared)'
    url_prefix = 'https://fileittax.sharefile.com/sf/v3/'
    headers = {
        'authorization': "Bearer " + token,
        'cache-control': "no-cache",
    }

    response = requests.request("GET","https://fileittax.sharefile.com/sf/v3/Items  ", headers=headers)
    print(response)
    print(response.reason)
    print(response.json().get('value'))
    root_folder_id = 'foe9344e-8793-4a4a-b793-e67f85b92f69'
    url1 = '{}Items/ByPath?path={}'.format(url_prefix, root_folder_path)
    response1 = requests.request("GET", url1, headers=headers)
    if response1.status_code == 200:
        item_id = response1.json().get('Id')
    else:
        print('getItemIdByPath {} {}'.format(response1.status_code, response1.content))


if __name__ == '__main__':
    token = authenticate()
    if token:
        get_root(token,"%*$*yano^OungM!*cH27")