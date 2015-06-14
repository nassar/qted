import sys
import argparse
import json
from collections import namedtuple
import time
import datetime

import db
import survey
import panel
import psv
import config

Response = namedtuple('Response', 'responseid data')
SurveyResponses = namedtuple('SurveyResponses', 'surveyid responses followupid')
Panel = namedtuple('Panel', 'panelid panel_name')
Recipient = namedtuple('Recipient', 'recipientid responseid')

def timestamp(pattern):
    t = time.time()
    dt = datetime.datetime.fromtimestamp(t).strftime(pattern)
    return dt

def print_response_data(response_data, responseids_panel):
    """
    Print a list of responses, placing an asterisk next to those matching a
    response ID in responseids_panel.
    """
    p = 'ResponseID | SurveyID | EndDate | PANEL\n'
    for sr in response_data:
        for r in sr.responses:
            p += '{:s} | {:s} | {:s} | {:s}{:s}\n'.format(
                                    r.responseid, sr.surveyid, 
                                    r.data['EndDate'], str(r.data['PANEL']),
                                    ' *' if r.responseid in responseids_panel
                                         else ''
                                    )
    print(psv.align(p))
    print()

def print_panels_and_recipients(panels_recipients, surveys_followups):
    if len(panels_recipients) == 0:
        return
    # Print survey and follow-up IDs
    p = 'SurveyID | FollowupID\n'
    for surveyid, followupid in surveys_followups:
        p += '{:s} | {:s}\n'.format(surveyid, followupid)
    print(psv.align(p))
    print()
    # Print panels
    p = 'PanelID | FollowupID | PanelName\n'
    for (surveyid, panel, recipients) in panels_recipients:
        p += '{:s} | {:s} | {:s}\n'.format( panel.panelid, surveyid,
                                                             panel.panel_name )
    print(psv.align(p))
    print()
    # Print recipients per panel
    p = 'RecipientID | ResponseID | PanelID\n'
    for (surveyid, panel, recipients) in panels_recipients:
        for r in recipients:
            p += '{:s} | {:s} | {:s}\n'.format( r.recipientid, r.responseid,
                                                                panel.panelid )
    print(psv.align(p))
    print()

def create_sr_panel(sr, followupid):
    # Create panel
    panel_name = '{:s} {:s}'.format(followupid, timestamp('%Y-%m-%d %H%M%S'))
    panelid = panel.create_panel(panel_name, sr)
    # Add recipients to panel
    recipients = []
    for r in sr.responses:
        first_name = r.data.get('CI_1_TEXT') or ''
        last_name = r.data.get('CI_2_TEXT') or ''
        email = r.data.get('CI_3_TEXT') or ''
#        email = config.get_config('user_email')
        ext_data_ref = r.responseid or ''
        marstat = r.data.get('marstat') or ''
        if marstat != '':
            embedded_data = {'marstat': marstat}
        else:
            embedded_data = ''
        recipientid = panel.add_recipient(panelid, first_name, last_name,
                                            email, ext_data_ref, embedded_data)
        if recipientid is None:
            print()
            print( 'Error adding recipient to panel, ResponseID = {:s}'.format(
                                                               r.responseid ) )
        else:
            recipients.append(Recipient(recipientid, r.responseid))
    # Return panel and recipients
    return ( Panel(panelid, panel_name), recipients )

def filter_responses_panel(sr_list):
    """
    Given a list of SurveyResponses, return a copy of the list that includes
    only reponses having PANEL == 1, and return also a list of their response
    IDs.
    """
    new_sr_list = []
    responseids_panel = []
    for sr in sr_list:
        new_r_list = []
        for r in sr.responses:
            if r.data['PANEL'] == 1:
                new_r_list.append(Response(r.responseid, r.data))
                responseids_panel.append(r.responseid)
        if len(new_r_list) > 0:
            new_sr_list.append( SurveyResponses( sr.surveyid, new_r_list,
                                                 sr.followupid) )
    return (new_sr_list, responseids_panel)

def run(args):
    print()
    # Pull data only for tracked surveys
    tracked_surveys = db.get_tracked_surveys()
    surveys = sorted(tracked_surveys, key=lambda s: s.surveyid)
    # Retrieve new response data
    sr_list = []
    for s in surveys:
        r = survey.retrieve_response_data(s.surveyid, s.last_responseid)
        # Convert to list of tuples
        r_list = [Response(k, v) for k, v in r.items()]
        r_sort = sorted(r_list, key=lambda d: d.data['EndDate'])
        if len(r_sort) > 0:
            followupid = db.get_next_followupid(s.surveyid)
            sr_list.append(SurveyResponses(s.surveyid, r_sort, followupid))
            if followupid is None and args.panel:
                print( 'No follow-up found for survey ' +
                       '{:s}; the panel will not be created'.format(s.surveyid)
                       )
                print()
            else:
                # Update the survey's last_response_id in the database
                if args.panel:
                    db.set_survey_last_responseid(s.id, r_sort[-1].responseid)
        else:
            if s.last_responseid is None:
                db.set_survey_last_responseid(s.id, '')
    # Select responses that indicate a follow-up (based on the value of PANEL)
    (sr_list_panel, responseids_panel) = filter_responses_panel(sr_list)
    # Print new response data
    print_response_data(sr_list, responseids_panel)
    # Create a panel per survey
    if args.panel and len(sr_list_panel) > 0:
        panels_recipients = []
        surveys_followups = []
        for sr in sr_list_panel:
            if sr.followupid is not None:
                surveys_followups.append( (sr.surveyid, sr.followupid) )
                (panel, recipients) = create_sr_panel(sr, sr.followupid)
                panels_recipients.append( (sr.followupid, panel, recipients) )
                db.queue_panel(panel.panelid, sr.followupid)
        print_panels_and_recipients(panels_recipients, surveys_followups)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted responses')
    parser.add_argument('--panel', help='create panels for follow-up surveys',
                        action="store_true")
    args = parser.parse_args()
    run(args)

