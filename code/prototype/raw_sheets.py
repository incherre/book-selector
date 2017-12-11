#This is a file for learning to use the Google Sheets API directly (instead of using gspread)
#Much of this is taken from the quickstart at developers.google.com/sheets/api/quickstart/python

import httplib2

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

#scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
scope =  [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive'
]

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name('book-selector-key.json', scope)
    http = credentials.authorize(httplib2.Http())
except Exception as e:
    print("Error: failed to authenticate")
    print(e)
    exit()

#Create new sheet start
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
#Create new sheet end

tester_email = 'test@example.com'
#Share the sheet start
#from developers.google.com/drive/v3/web/manage-sharing
def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))

drive_service = discovery.build('drive', 'v3', http=http)

batch = drive_service.new_batch_http_request(callback=callback)
user_permission = {
    'type': 'user',
    'role': 'owner', #or writer
    'emailAddress': tester_email
}
batch.add(drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
        transferOwnership=True, #only required for owner permission
))
batch.execute()
#Share the sheet end
