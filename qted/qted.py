#!/usr/bin/env python3

import sys
import subprocess

help_text = '''
qted - a toolkit for scheduling Qualtrics surveys

usage: qted COMMAND [ARGUMENTS]...

where COMMAND is one of:
config       - modify the configuration file
debug-server - send requests to the Qualtrics server
responses    - retrieve response data for tracked surveys and optionally create
               panels for any responses indicating a follow-up
send         - send invitations to panels for follow-up surveys
surveys      - list all surveys in account
track        - add or remove surveys to tracking list
            '''

def help():
    print(help_text)

def valid_command(cmd):
    return cmd in ( 'config',
                    'debug-server',
                    'responses',
                    'send',
                    'surveys',
                    'track' )

def run_command(argv):
    cmd = argv[1]
    if valid_command(cmd):
        arg = argv[2:]
        program = 'qted-' + cmd + '.py'
        proc = ['python3', program] + arg
        subprocess.call(proc)
    else:
        thing = 'option' if cmd.startswith('-') else 'command'
        print('Unknown {:s} "{:s}"'.format(thing, cmd))
        print()
        help()

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2 or argv[1] in ('-h', '--help'):
        help()
    else:
        run_command(argv)

