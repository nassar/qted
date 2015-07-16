import argparse

import db
import panel
import psv

def print_sent(panels):
    """
    """
    p = 'SurveyID | PanelID | MessageID | SendDate\n'
    for panel in panels:
        senddate_notime = panel.senddate.split(' ')[0]
        p += '{:s} | {:s} | {:s} | {:s}\n'.format(panel.surveyid,
                                                  panel.panelid,
                                                  panel.messageid,
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

def send(panels, message):
    panels_sent = []
    for p in panels:
        # Schedule invitation
        r = panel.send_survey_to_panel(surveyid=p.surveyid,
                                       senddate=p.senddate,
                                       messageid=p.messageid,
                                       panelid=p.panelid)
        # TODO add to panels_sent only if successful
        panels_sent.append(p)
        # If send was successful, set panel invited to True in database
        if r is not None:
            result = r.get('Result')
            if result is not None:
                success = result.get('Success')
                if success is not None and success == True:
                   db.update_panel_by_panelid(p.panelid, invited=True)
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

