import argparse
from datetime import date
from dateutil.relativedelta import relativedelta
from collections import namedtuple

import db
import panel
import psv

SentPanels = namedtuple('SentPanels', 'panel time_interval senddate messageid')

def print_sent(sent_panels):
    """
    """
    p = 'SurveyID | PanelID | MessageID | SendDate\n'
    for sp in sent_panels:
        senddate_notime = sp.senddate.split(' ')[0]
        p += '{:s} | {:s} | {:s} | {:s}\n'.format(sp.panel.surveyid,
                                                  sp.panel.panelid,
                                                  sp.messageid,
                                                  senddate_notime)
    print(psv.align(p))
    print()

def retrieve_panels(panelid, all):
    if all:
        panels = db.select_panel_by_invited(invited=False)
    else:
        p = db.select_panel_by_panelid(panelid)
        if p.invited:
            print('Panel has already been invited')
            print()
            panels = None
        else:
            panels = [ p ]
    return panels

def calculate_send_date(months):
    calc_date = date.today() + relativedelta(months=months)
    return str(calc_date) + ' 00:00:00'

def send(panels, message):
    panels_sent = []
    for p in panels:
        # Get details associated with follow-up
        followup = db.select_followup_by_followupid(p.surveyid)
        senddate = calculate_send_date(int(followup.time_interval))
        messageid = followup.messageid
        # Schedule invitation
        r = panel.send_survey_to_panel(surveyid=p.surveyid,
                                       senddate=senddate,
                                       messageid=messageid,
                                       panelid=p.panelid)
        # TODO add to panels_sent only if successful
        sp = SentPanels(p, followup.time_interval, senddate, messageid)
        panels_sent.append(sp)
        # TODO if send was successful, set panel invited to True in database
        # {'Result': {'Success': True, 'DistributionQueueID': 'EMD_6hP4N4bXrxGGQFD', 'EmailDistributionID': 'EMD_6hP4N4bXrxGGQFD'}, 'Meta': {'Debug': '', 'Status': 'Success'}}
    print_sent(panels_sent)

def run(args):
    panels = retrieve_panels(args.panelid, args.all)
    if panels is not None:
        send(panels, args.message)

def validate_args(args):
    if args.panelid is None and not args.all:
        print('No panel ID was specified')
        print()
        return False
    if args.panelid is not None and args.all:
        print('Option --all cannot be used with a panel ID')
        print()
        return False
    return True

if __name__ == '__main__':
    print()
    parser = argparse.ArgumentParser(prog='qted send')
    parser.add_argument('panelid',
                        nargs='?',
                        help='panel ID containing the list of recipients')
    parser.add_argument('--all',
                        help="send to all panels that haven't been invited",
                        action='store_true')
    parser.add_argument('--message',
                        help='message ID to send to the panel')
    args = parser.parse_args()
    if validate_args(args):
        run(args)

