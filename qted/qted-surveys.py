import argparse

import survey

def run(args):
    surveys = survey.retrieve_surveys()
    print()
    survey.print_surveys(surveys, args.verbose)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='qted surveys')
    parser.add_argument('-v', '--verbose', help='show survey details',
                        action="store_true")
    args = parser.parse_args()
    run(args)

