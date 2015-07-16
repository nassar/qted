import argparse

import db
import psv

def run(args):
    # TODO expand IDs as in qted-track.track_survey()
    # TODO rewrite db.set_follow_up_surveys() to take a single followupid
    db.set_follow_up_surveys(args.baseline, args.followupid, args.message,
                             args.time)
    # TODO provide a way to delete a follow-up, via db.delete_follow_up_surveys

def validate_args(args):
    # TODO validate command line arguments
    return True

if __name__ == '__main__':
    print()
    parser = argparse.ArgumentParser(prog='qted followup')
    parser.add_argument('followupid',
                        nargs='?',
                        help='Survey ID of the follow-up survey')
    parser.add_argument('--baseline',
                        help='Survey ID of the baseline survey')
    parser.add_argument('--message',
                        help='Message ID to use for the follow-up survey')
    parser.add_argument('--time',
                        help='Time interval in months')
    args = parser.parse_args()
    if validate_args(args):
        run(args)

