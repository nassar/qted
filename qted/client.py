import argparse
import requests
import json
import copy

import config

def request(params):
    """
    Sends a request to the Qualtrics server and retrieves the response.  Given
    a dictionary params, returns a 2-tuple (request, response).  The values
    for User and Token are supplied from the configuration file if omitted from
    params.  Only JSON responses are supported.
    """
    p = copy.deepcopy(params)
    if p.get('User') is None:
        p['User'] = config.get_config('qt_user')
    if p.get('Token') is None:
        p['Token'] = config.get_config('qt_token')
    if p.get('Version') is None:
        p['Version'] = '2.4'
    p['Format'] = 'JSON'
    response = requests.post( config.get_config('qt_server'), params=p )
    return (p, response.json())

if __name__ == '__main__':
    pass

