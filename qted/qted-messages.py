import argparse

import message

def run(args):
    messages = message.retrieve_messages()
    print()
    message.print_messages(messages)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted messages')
    args = parser.parse_args()
    run(args)

