from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/script-python-forms-quickstart.json
SCOPES =  'https://www.googleapis.com/auth/drive '
SCOPES += 'https://www.googleapis.com/auth/forms '
CLIENT_SECRET_FILE = 'book-selector-userauth-key.json'
APPLICATION_NAME = 'Google Apps Script Execution API Python Forms'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'script-python-forms-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Apps Script Execution API.

    Creates a Apps Script Execution API service object and uses it to call an
    Apps Script function to print out a list of folders in the user's root
    directory.
    """
    SCRIPT_ID = 'ENTER_YOUR_SCRIPT_ID_HERE'
    user_name = 'Enter a username here'
    user_email = 'Enter a user email here'
    
    scope =  [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]
    service_account_creds = ServiceAccountCredentials.from_json_keyfile_name('book-selector-key.json', scope)
    service_account_email = service_account_creds._service_account_email

    # Authorize and create a service object.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('script', 'v1', http=http)

    # Create an execution request object.
    request = {"function": "makePollForm",
               "parameters": [service_account_email,
                              ["Book1", "Book2", "Book3", "Book4"]]
              }

    try:
        # Make the API request.
        response = service.scripts().run(body=request,
                scriptId=SCRIPT_ID).execute()

        if 'error' in response:
            # The API executed, but the script returned an error.

            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # an list of stack trace elements.
            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                        trace['lineNumber']))
        else:
            #The structure for makeBooksForm should be a dict with form_id and form_url
            formInfo = response['response'].get('result', {})
            
            if not formInfo:
                print('No form info returned!')
            else:
                if formInfo['form_id']:
                    print('Form id: ' + formInfo['form_id'])
                if formInfo['form_url']:
                    print('Form url: ' + formInfo['form_url'])
    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        print(e.content)

if __name__ == '__main__':
    main()
