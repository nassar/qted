import client
import psv

def retrieve_surveys(sort_key='SurveyCreationDate'):
    """
    Retrieve the list of surveys and return them as a list of dictionaries.
    """
    p = { 'Request': 'getSurveys' }
    (request, response) = client.request(p)
    surveys = response['Result']['Surveys']
    return sorted(surveys, key=lambda s: s[sort_key])

def print_surveys(surveys, verbose=False):
    """
    Print a list of surveys, with more detail if verbose is True.
    """
    p = 'SurveyID | SurveyName'
    if verbose:
        p += ' | SurveyStatus | SurveyCreationDate'
    p += '\n'
    for s in surveys:
        p += '{:s} | {:s}'.format(s['SurveyID'], s['SurveyName'])
        if verbose:
            p += ' | {:s} | {:s}'.format(
                                    s['SurveyStatus'], s['SurveyCreationDate'])
        p += '\n'
    print(psv.align(p))
    print()

def retrieve_surveys_by_ids(surveyids):
    """
    Given a list of survey IDs (or the first few characters of survey IDs),
    return a corresponding list with each element consisting of a list having
    the requested surveyID as the first element followed by one or more surveys
    retrieved from the Qualtrics server that match the given ID.
    """
    surveys = retrieve_surveys()
    matches = [ [id] + [s for s in surveys if s['SurveyID'].startswith(id)]
                for id in surveyids ]
    return matches

def locate_surveys(surveyids):
    """
    Given a partial or complete surveyid: return a matching survey's ID; or if
    multple IDs match then print the matching surveys and return None; or if
    there is no match then print an error message and return None.
    """
    surveys_list = retrieve_surveys_by_ids(surveyids)
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

def retrieve_response_data(surveyid, last_responseid):
    """
    Retrieve the list of new response data for the given surveyid and since the
    given last_responseid, and return them as a list of dictionaries.
    """
    p = { 'Request': 'getLegacyResponseData',
          'SurveyID': surveyid }
    if last_responseid is not None and last_responseid != '':
        p['LastResponseID'] = last_responseid
    (request, response_data) = client.request(p)
    return response_data if type(response_data) is dict else {}

if __name__ == '__main__':
    pass

