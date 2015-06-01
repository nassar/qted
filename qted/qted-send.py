import argparse

import survey

def run(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted send')
    parser.add_argument('panelid', nargs='?',
        help='panel ID containing the list of recipients')
    parser.add_argument('--all',
        help="send to all panels that haven't been invited")
    args = parser.parse_args()
    run(args)

