import client
import config
import psv

def retrieve_messages():
    """
    Retrieve the list of messages and return them as a dictionary.
    """
    p = { 'Request': 'getLibraryMessages',
          'LibraryID': config.get_config('qt_library') }
    (request, response) = client.request(p)
    return response.get('Result')

def print_messages(messages):
    """
    Print a list of messages.
    """
    p = 'Category | MessageID | MessageName\n'
    messages_list = [(category, data)
                     for category, data in messages.items()]
    messages_sort = sorted(messages_list, key=lambda m: m[0])
    for category, data in messages_sort:
        if isinstance(data, dict):
            message_list = [(messageid, messagename)
                            for messageid, messagename in data.items()]
            message_sort = sorted(message_list, key=lambda m: m[1])
            for messageid, messagename in message_sort:
                p += '{:s} | {:s} | {:s}\n'.format(category, messageid,
                                                   messagename)
    print(psv.align(p))
    print()

if __name__ == '__main__':
    pass

