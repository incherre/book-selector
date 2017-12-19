#This is a file for learning to use the Google Sheets API directly (instead of using gspread)
#Much of this is taken from the quickstart at developers.google.com/sheets/api/quickstart/python

import httplib2
import os

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import discovery

#scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
scope =  [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
'https://www.googleapis.com/auth/forms',
]
SCOPES = scope
CLIENT_SECRET_FILE = 'book-selector-userauth-key.json'
APPLICATION_NAME = 'Test Script for Book Selector'

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name('book-selector-key.json', scope)
    http = credentials.authorize(httplib2.Http())
except Exception as e:
    print("Error: failed to authenticate")
    print(e)
    exit()

#Create new sheet
def newSheet(credentials):
    sheets_service = discovery.build('sheets', 'v4', credentials=credentials)
    spreadsheet_body = {
        "properties": {
            "title": "MyCustomNewSpreadsheet"
        },
        "sheets": [{
            "properties": {
                "title": "MyCustomDefaultSheet",
                "index": 0
            }
        }]
    }
    request = sheets_service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    file_id = response['spreadsheetId']
    return file_id

#Share the sheet
#from developers.google.com/drive/v3/web/manage-sharing
def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))

def shareWith(http, file_id, email):
    drive_service = discovery.build('drive', 'v3', http=http)

    batch = drive_service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'owner', #or writer
        'emailAddress': email
    }
    batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
            transferOwnership=True, #only required for owner permission
    ))
    batch.execute()

#Creating a form
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
    credential_path = os.path.join(credential_dir, 'appscript-credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)#, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

apps_script_api_id = "api id"
def createForm(script_id):
    #got to find a way around:
    #https://issuetracker.google.com/issues/36763096
    s_credentials = get_credentials()
    s_http = credentials.authorize(httplib2.Http())
    script_service = discovery.build('script', 'v1', http=s_http)

    request = {"function": "makeTestForm",
               "parameters": [credentials._service_account_email],}

    response = script_service.scripts().run(body=request, scriptId=script_id).execute()

    print(str(response))

tester_email = 'test@example.com'
#file_id = newSheet(credentials)
#shareWith(http, file_id, tester_email)
createForm(apps_script_api_id)


