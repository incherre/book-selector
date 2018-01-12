import books_common

import os
import httplib2
import time

from apiclient import discovery
from apiclient import errors

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools

def get_credentials(credential_name, client_secret_file, scopes, application_name):
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, credential_name)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scopes)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store)
    return credentials

class AppsScriptError(Exception):
    pass

class SheetsLocation(books_common.Location):
    '''A class representing where a book is stored when used with GoogleDocsBot.'''

    def __init__(self):
        raise NotImplementedError('Abstract method "__init__" not implemented')

    def compare(self, other):
        raise NotImplementedError('Abstract method "compare" not implemented')

class GoogleDocsBot(books_common.DataIO):
    '''A class representing the functions to communicate with Google Drive.'''

    service_scope = ['https://www.googleapis.com/auth/drive',
                     'https://www.googleapis.com/auth/spreadsheets']

    appsscript_scope = ['https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/forms',
                        'https://www.googleapis.com/auth/userinfo.email']

    userSheetName = 'BookClubUsers'

    def __init__(self, credential_path, client_secret_path, app_name, credential_name, script_id):
        if isinstance(app_name, str):
            self.app_name = app_name
        else:
            raise TypeError("Provided application name not a string.")

        if isinstance(script_id, str):
            self.script_id = script_id
        else:
            raise TypeError("Provided script_id not a string.")

        try:
            service_creds = ServiceAccountCredentials.from_json_keyfile_name(credential_path, self.service_scope)
            drive_http = service_creds.authorize(httplib2.Http())
            self.drive_service = discovery.build('drive', 'v3', http=drive_http)
            self.sheets_service = discovery.build('sheets', 'v4', credentials=service_creds)
            self.service_email = service_creds._service_account_email
        except FileNotFoundError:
            print('File: "' + str(credential_path) + '" was not found.')
            raise

        try:
            appsscript_creds = get_credentials(credential_name, client_secret_path, self.appsscript_scope, app_name)
            appsscript_http = appsscript_creds.authorize(httplib2.Http())
            self.appsscript_service = discovery.build('script', 'v1', http=appsscript_http)

            email_request = {"function": "getEmail", "parameters": []}
            email_response = self.appsscript_service.scripts().run(
                body=email_request,scriptId=self.script_id).execute()
            
            if 'error' in email_response:
                error = email_response['error']['details'][0]
                raise AppsScriptError(error)
            else:
                self.admin_email = email_response['response'].get('result', str)

            if self.admin_email == '':
                raise AppsScriptError('Failed to retrieve user email.')
        except FileNotFoundError:
            print('File: "' + str(client_secret_path) + '" was not found.')
            raise

    def getFileList(self):
        '''Returns a list of files accessible by the service account.'''
        files_results = self.drive_service.files().list(
            fields="nextPageToken, files(id, name)").execute()
        files = files_results.get('files', [])
        nextPageToken = files_results.get('nextPageToken')
        
        while nextPageToken and nextPageToken != '':
            #make sure to get the full list if required
            files_results = drive_service.files().list(
                pageToken=nextPageToken,
                fields="nextPageToken, files(id, name)").execute()
            files += files_results.get('files', [])
            nextPageToken = files_results.get('nextPageToken')

        return files

    def makeNewBookClub(self, shouldPrint=True, retryShare=5):
        '''Creates the document structure for a new book club. Returns success.'''

        #start checking for old book club code
        files = self.getFileList()
        if files:
            for item in files:
                if item['name'] == self.userSheetName:
                    if shouldPrint:
                        print('Book Club already exists under this bot.')
                    return False #Can't make a new book club when there is already one
        #end checking for old book club code

        #start creating new book club code
        spreadsheet_body = {
            "properties": {
                "title": self.userSheetName
            },
            "sheets": [{
                "properties": {
                    "title": "Users",
                    "index": 0
                }
            }]
        }
        new_sheet_request = self.sheets_service.spreadsheets().create(body=spreadsheet_body)
        try:
            new_sheet_response = new_sheet_request.execute() #make the new spreadsheet
        except errors.HttpError:
            if shouldPrint:
                print('Failed to create the new User spreadsheet')
            return False
        new_sheet_file_id = new_sheet_response['spreadsheetId']
        #end creating new book club code

        #start sharing code
        user_permission = {
            'type': 'user',
            'role': 'owner',
            'emailAddress': self.admin_email
        }
        share_request = self.drive_service.permissions().create(
                fileId=new_sheet_file_id,
                body=user_permission,
                fields='id',
                transferOwnership=True) #only required for 'owner' permission
        
        for i in range(retryShare): #Try some number (default 5) of times
            try:
                share_response = share_request.execute() #share the new spreadsheet
            except errors.HttpError:
                if i < (retryShare - 1):
                    if shouldPrint:
                        print('Failed to share, pausing for a short bit')
                    time.sleep(1) #delay prevents "InternalServerError"s
                    if shouldPrint:
                        print('Done pausing, trying again')
                else:
                    if shouldPrint:
                        print('Tried and failed the maximum number of times.')
                    raise #could try to delete the document first...
            else:
                break
        #end sharing code

        return True

    def getUserNames(self):
        raise NotImplementedError('Abstract method "getUserNames" not implemented')

    def getUserInfo(self, user):
        raise NotImplementedError('Abstract method "getUserInfo" not implemented')

    def getUserBooks(self, user):
        raise NotImplementedError('Abstract method "getUserBooks" not implemented')

    def getHistory(self):
        raise NotImplementedError('Abstract method "getHistory" not implemented')

    def getCurrentPoll(self):
        raise NotImplementedError('Abstract method "getCurrentPoll" not implemented')

    def createUser(self, user):
        raise NotImplementedError('Abstract method "createUser" not implemented')

    def removeBook(self, book):
        raise NotImplementedError('Abstract method "removeBook" not implemented')

    def newPoll(self, poll):
        raise NotImplementedError('Abstract method "newPoll" not implemented')

    def closePoll(self, poll):
        raise NotImplementedError('Abstract method "closePoll" not implemented')

    def addWinner(self, book):
        raise NotImplementedError('Abstract method "addWinner" not implemented')
