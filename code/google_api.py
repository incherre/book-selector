import books_common

import os
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
                             'https://www.googleapis.com/auth/forms']
    
    def __init__(self, credential_path, client_secret_path, app_name, credential_name):
        if isinstance(app_name, str):
            self.app_name = app_name
        else:
            raise TypeError("Provided application name not a string.")
        
        try:
            self.service_creds = ServiceAccountCredentials.from_json_keyfile_name(credential_path, self.service_scope)
        except FileNotFoundError:
            print('File: "' + str(credential_path) + '" was not found.')
            raise

        try:
            get_credentials(credential_name, client_secret_path, self.appsscript_scope, app_name)
        except FileNotFoundError:
            print('File: "' + str(client_secret_path) + '" was not found.')
            raise
        

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
