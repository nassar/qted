import argparse

import db
import survey
import psv

def run(args):
    ids_select = [args.followupid, args.baselineid]
    ids = survey.locate_surveys(ids_select)
    followupid, baselineid = ids[0], ids[1]
    db.add_followup(followupid, baselineid, args.messageid, args.months)

def validate_args(args):
    # TODO validate command line arguments
    return True

# TODO provide a way to delete all follow-ups, via db.delete_follow_up_surveys,
# or a single follow-up.
if __name__ == '__main__':
    print()
    parser = argparse.ArgumentParser(prog='qted followup')
    parser.add_argument('followupid',
                        nargs='?',
                        help='Survey ID of the follow-up survey')
    parser.add_argument('--baselineid',
                        help='Survey ID of the baseline survey')
    # TODO support partial messageid as we do with surveyids
    parser.add_argument('--messageid',
                        help='Message ID to use for the follow-up survey')
    parser.add_argument('--months',
                        help='Time interval in months')
    args = parser.parse_args()
    if validate_args(args):
        run(args)

