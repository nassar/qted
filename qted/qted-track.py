import os
import argparse
import requests
import json
import configparser

import db
import survey

def list_tracked_surveys():
    """
    Print a list of all surveys that are currently tracked.
    """
    surveys = db.get_all_surveys()
    tracked_surveyids = [s.surveyid for s in surveys if s.tracked == True]
    qt_surveys = survey.retrieve_surveys()
    tracked_qt_surveys = [s for s in qt_surveys
                          if s['SurveyID'] in tracked_surveyids]
    survey.print_surveys(tracked_qt_surveys)

def locate_surveys(surveyids):
    """
    Given a partial or complete surveyid: return a matching survey's ID; or if
    multple IDs match then print the matching surveys and return None; or if
    there is no match then print an error message and return None.
    """
    surveys_list = survey.retrieve_surveys_by_ids(surveyids)
    for surveys in surveys_list:
        surveyid = surveys[0]
        if len(surveys) == 1:
            print('No survey matching ID "{:s}" was found'.format(surveyid))
            print()
            return None
        if len(surveys) > 2:
            print('ID "{:s}" matches more than one survey:'.format(surveyid))
            survey.print_surveys(surveys[1:])
            print()
            return None
    return [ s[1]['SurveyID'] for s in surveys_list ]

def track_survey(surveyid_select, track, follow_up_select):
    """
    Track or stop tracking the survey specified by surveyid, based on the value
    of track.  If track == True, follow_up can specify a list of follow-up
    survey IDs.
    """
    ids_select = [surveyid_select] + follow_up_select
    ids = locate_surveys(ids_select)
    surveyid = ids[0]
    follow_up = ids[1:]
    db.track_survey(surveyid, track)
    print( 'Survey {:s} will {:s}be tracked'.format( surveyid,
                                                    '' if track else 'not ' ) )
    print()
    # Set or delete the list of follow-up surveys
    if track:
        db.set_follow_up_surveys(surveyid, follow_up)
    else:
        db.delete_follow_up_surveys(surveyid)

def run(args):
    print()
    if args.surveyid is None and args.stop == False:
        list_tracked_surveys()
    else:
        if args.surveyid is None:
            print('No survey ID was specified')
            print()
            return
        if args.stop and args.follow_up:
            print('The --stop option cannot be used with --follow-up')
            print()
            return
        follow_up_list = ( [s.strip() for s in args.follow_up.split(',')]
                           if args.follow_up is not None else [] )
        track_survey(surveyid_select=args.surveyid, track=(not args.stop),
                     follow_up_select=follow_up_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted track')
    parser.add_argument('surveyid', nargs='?',
        help='survey ID to track (or if omitted, show tracked surveys)')
    parser.add_argument('--stop', help='stop tracking the survey',
                        action="store_true")
    parser.add_argument('--follow-up',
                        help='comma-separated list of follow-up survey IDs')
    args = parser.parse_args()
    run(args)

