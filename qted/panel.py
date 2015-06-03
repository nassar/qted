import config
import client

def create_panel(panel_name, sr):
    p = { 'Request': 'createPanel',
          'LibraryID': config.get_config('qt_library'),
          'Name': panel_name }
    (request, response) = client.request(p)
    panelid = response['Result']['PanelID']
    return panelid

def add_recipient(panelid, first_name, last_name, email, ext_data_ref,
                        embedded_data):
    p = { 'Request': 'addRecipient',
          'LibraryID': config.get_config('qt_library'),
          'PanelID': panelid }
    if first_name is not None and first_name != '':
        p['FirstName'] = first_name
    if last_name is not None and last_name != '':
        p['LastName'] = last_name
    if email is not None and email != '':
        p['Email'] = email
    if ext_data_ref is not None and ext_data_ref != '':
        p['ExternalDataRef'] = ext_data_ref
    if embedded_data is not None and embedded_data != {}:
        for k, v in embedded_data.items():
            p['ED[{:s}]'.format(k)] = v
    (request, response) = client.request(p)
    result = response.get('Result')
    if result is None or result == '':
        return None
    recipientid = result.get('RecipientID')
    if recipientid is None or recipientid == '':
        return None
    return recipientid

def send_survey_to_panel(surveyid, senddate, messageid, panelid):
    p = { 'Request': 'sendSurveyToPanel',
          'SurveyID': surveyid,
          'SendDate': senddate,
          'SentFromAddress': config.get_config('user_email'),
          'FromEmail': config.get_config('user_email'),
          'FromName': 'Survey Creator',
          'Subject': 'Follow-up Survey',
          'MessageID': messageid,
          'MessageLibraryID': config.get_config('qt_library'),
          'PanelID': panelid,
          'PanelLibraryID': config.get_config('qt_library'),
          'ExpirationDate': '3000-01-01 00:00:00' }
    (request, response) = client.request(p)
    return response

if __name__ == '__main__':
    create_panel()
    pass

