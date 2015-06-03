import argparse

import db
import panel

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

def send(panels):
    for p in panels:
        r = panel.send_survey_to_panel(surveyid=p.surveyid,
                                       senddate='2015-06-03 17:20:00',
                                       messageid='MS_03uJDRmpiNDfAfX',
                                       panelid=p.panelid)
        print(r)
        # TODO if send was successful, set panel invited to True in database
        # {'Result': {'Success': True, 'DistributionQueueID': 'EMD_6hP4N4bXrxGGQFD', 'EmailDistributionID': 'EMD_6hP4N4bXrxGGQFD'}, 'Meta': {'Debug': '', 'Status': 'Success'}}

def run(args):
    panels = retrieve_panels(args.panelid, args.all)
    if panels is not None:
        send(panels)

def validate_args(args):
    if args.panelid is None and not args.all:
        print('No panel ID was specified')
        print()
        return False
    elif args.panelid is not None and args.all:
        print('Option --all cannot be used with a panel ID')
        print()
        return False
    else:
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted send')
    parser.add_argument('panelid',
                        nargs='?',
                        help='panel ID containing the list of recipients')
    parser.add_argument('--all',
                        help="send to all panels that haven't been invited",
                        action='store_true')
    args = parser.parse_args()
    if validate_args(args):
        run(args)

