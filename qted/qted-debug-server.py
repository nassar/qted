import argparse
import requests
import json

import client

def run(args):
    params = json.loads(args.params)
    (request, response) = client.request(params)
    print('REQUEST ----------------------------------------------------------')
    print(json.dumps(request, ensure_ascii=False, indent=4))
    print('RESPONSE ---------------------------------------------------------')
    print(json.dumps(response, indent=4))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted debug-server')
    parser.add_argument("params",
        help='''
             parameters for request to server, in JSON format, e.g.
             '{"Request": "getSurveys"}'
             ''')
    args = parser.parse_args()
    run(args)

