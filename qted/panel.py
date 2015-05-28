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

if __name__ == '__main__':
    create_panel()
    pass

