import os
import argparse
import requests
import json
import configparser

import db
import survey
import psv

def print_tracked_surveys(surveys):
    """
    Print a list of surveys, with more detail if verbose is True.
    """
    p = 'SurveyID | FollowupIDs\n'
    for s in surveys:
        p += '{:s} | {:s}\n'.format(s.surveyid, s.followupids)
    print(psv.align(p))
    print()

def list_tracked_surveys():
    """
    Print a list of all surveys that are currently tracked.
    """
    surveys = db.get_all_surveys()
    tracked = [s for s in surveys if s.tracked == True]
    print_tracked_surveys(tracked)

def track_survey(surveyid_select, track):
    """
    Track or stop tracking the survey specified by surveyid, based on the value
    of track.
    """
    ids = survey.locate_surveys([surveyid_select])
    surveyid = ids[0]
    db.track_survey(surveyid, track)

def run(args):
    print()
    if args.surveyid is None and args.stop == False:
        list_tracked_surveys()
    else:
        if args.surveyid is None:
            print('No survey ID was specified')
            print()
            return
        track_survey(surveyid_select=args.surveyid, track=(not args.stop))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted track')
    parser.add_argument('surveyid',
                        nargs='?',
               help='survey ID to track (or if omitted, show tracked surveys)')
    parser.add_argument('--stop', help='stop tracking the survey',
                        action="store_true")
    args = parser.parse_args()
    run(args)

