import os
import argparse
import requests
import json
import configparser

import config

def run(args):
    print()
    config.set_config(args.name, args.value)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted config')
    parser.add_argument("name",
        help="name of configuration variable to set")
    parser.add_argument("value",
        help="new value of configuration variable")
    args = parser.parse_args()
    run(args)

