import books_common

import os
import httplib2
import time
import string

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

def try_request_n_retries(request, times):
    for i in range(times):
        try:
            result = request.execute()

            if 'error' in result:
                error = result['error']['details'][0]
                raise AppsScriptError(error)
            
        except errors.HttpError:
            if i == times - 1:
                raise
            else:
                time.sleep(1)
        else:
            return result

def colNumber2colLetter(colNumber):
    colLetter = ''
    unconverted_part = colNumber
    while unconverted_part > 0:
        letter_index = (unconverted_part - 1) % 26
        colLetter = string.ascii_uppercase[letter_index] + colLetter
        unconverted_part = int((unconverted_part - letter_index - 1) / 26)
    return colLetter

def getA1Notation(sheetName, col1, row1, col2, row2):
    A1notation = "'" + sheetName + "'!"
    A1notation += colNumber2colLetter(col1) + str(row1) + ':'
    A1notation += colNumber2colLetter(col2) + str(row2)
    return A1notation

class AppsScriptError(Exception):
    pass

class SpreadsheetFormatError(Exception):
    pass

class FormLocation(books_common.Location):
    '''A class representing where a book is stored when used with GoogleDocsBot.'''

    def __init__(self, formId, responseId):
        if isinstance(formId, str):
            self.formId = formId
        else:
            raise TypeError("Provided form ID not a string.")

        if isinstance(responseId, str):
            self.responseId = responseId
        else:
            raise TypeError("Provided response ID not a string.")

    def compare(self, other):
        same = True
        same = same and isinstance(other, FormLocation)
        same = same and self.formId == other.formId
        same = same and self.responseId == other.responseId
        return same

class GoogleDocsBot(books_common.DataIO):
    '''A class representing the functions to communicate with Google Drive.'''

    service_scope = ['https://www.googleapis.com/auth/drive',
                     'https://www.googleapis.com/auth/spreadsheets']

    appsscript_scope = ['https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/forms',
                        'https://www.googleapis.com/auth/userinfo.email']

    infoSpreadNames = ('BookClubInfo', 'Users', 'History', 'GlobalInfo')
    userSheetWidth = 4
    historySheetWidth = 4
    pollIdPos = (1, 1)

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

    def getBookClubInfoSheetID(self):
        '''Returns the file id of the sheet used to store book club information.'''

        if not hasattr(self, 'bookClubInfoSheetID'):
            files = self.getFileList()
            self.bookClubInfoSheetID = None
            if files:
                for item in files:
                    if item['name'] == self.infoSpreadNames[0]:
                        self.bookClubInfoSheetID = item['id']

            if not self.bookClubInfoSheetID:
                del self.bookClubInfoSheetID
                raise SpreadsheetFormatError('No User spreadsheet found.')

        return self.bookClubInfoSheetID

    def getUserTable(self, retryGet=5, fetchNum=10):
        '''Returns a matrix of user records.'''

        if not hasattr(self, 'userTable'):
            userSheetId = self.getBookClubInfoSheetID()

            rangeStart = 1
            userInfo = {}

            rangeStr = getA1Notation(self.infoSpreadNames[1], 1, rangeStart, self.userSheetWidth, (rangeStart + fetchNum - 1))
            request = self.sheets_service.spreadsheets().values().get(
                majorDimension='ROWS', spreadsheetId=userSheetId, range=rangeStr)
            result = try_request_n_retries(request, retryGet)
            values = result.get('values', [])

            while values != []:
                for user in values:
                    if user != []:
                        userInfo[user[0]] = user

                rangeStart += fetchNum
                rangeStr = getA1Notation(self.infoSpreadNames[1], 1, rangeStart, self.userSheetWidth, (rangeStart + fetchNum - 1))

                request = self.sheets_service.spreadsheets().values().get(
                    majorDimension='ROWS', spreadsheetId=userSheetId, range=rangeStr)
                result = try_request_n_retries(request, retryGet)
                values = result.get('values', [])

            self.userTable = userInfo

        return self.userTable

    def makeNewBookClub(self, shouldPrint=True, retryShare=5):
        '''Creates the document structure for a new book club. Returns success.'''

        #start checking for old book club code
        files = self.getFileList()
        if files:
            for item in files:
                if item['name'] == self.infoSpreadNames[0]:
                    if shouldPrint:
                        print('Book Club already exists under this bot.')
                    return False #Can't make a new book club when there is already one
        #end checking for old book club code

        #start creating new book club code
        spreadsheet_body = {
            "properties": {
                "title": self.infoSpreadNames[0]
            },
            "sheets": [{
                "properties": {
                    "title": self.infoSpreadNames[1],
                    "index": 0
                }},
                {
                "properties": {
                    "title": self.infoSpreadNames[2],
                    "index": 1
                }}
            ]
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

        share_response = try_request_n_retries(share_request, retryShare) #share the new spreadsheet
        #end sharing code

        return True

    def getUserNames(self, retryGet=5, fetchNum=10):
        '''Returns a list of usernames. Optional parameter fetchNum controls how many are fetched at once.'''

        userTable = self.getUserTable(retryGet=retryGet, fetchNum=fetchNum)

        userNames = list(userTable.keys())

        return userNames

    def getUserInfo(self, userName, retryGet=5, fetchNum=10):
        '''Returns a user's information. Optional parameter fetchNum controls how many are fetched at once.'''

        userInfo = []
        userTable = self.getUserTable(retryGet=retryGet, fetchNum=fetchNum)

        if userName in userTable:
            userInfo = userTable[userName]

        if len(userInfo) >= self.userSheetWidth:
            return books_common.User(userInfo[0], userInfo[1], [], userInfo[2])
        else:
            return userInfo

    def getUserBooks(self, user, retryGet=5, fetchNum=10):
        '''Returns the list of books entered by the user and updates the user object's book list.'''

        userName = user.getUserName()
        userFormID = None
        userTable = self.getUserTable(retryGet=retryGet, fetchNum=fetchNum)

        if userName in userTable:
            userFormID = userTable[userName][3]
        else:
            raise SpreadsheetFormatError('Requested User does not exist.')

        getbooks_function = {"function": "getBookList", "parameters": [userFormID]}
        getbooks_request = self.appsscript_service.scripts().run(body=getbooks_function,scriptId=self.script_id)
        getbooks_response = try_request_n_retries(getbooks_request, 5)

        rawbooks_list = getbooks_response['response'].get('result', [])
        books_list = [books_common.Book(i['title'], i['authorFirstName'], i['authorLastName'],
                                        FormLocation(userFormID, i['formResponseId']), self)
                      for i in rawbooks_list]

        user.replaceBooks(books_list)

        return books_list

    def getHistory(self, retryGet=5, fetchNum=10):
        '''Gets a list of books that have previously won a contest.'''

        if not hasattr(self, 'history'):
            userSheetId = self.getBookClubInfoSheetID()

            rangeStart = 1
            history = []

            rangeStr = getA1Notation(self.infoSpreadNames[2], 1, rangeStart, self.historySheetWidth, (rangeStart + fetchNum - 1))
            request = self.sheets_service.spreadsheets().values().get(
                majorDimension='ROWS', spreadsheetId=userSheetId, range=rangeStr)
            result = try_request_n_retries(request, retryGet)
            values = result.get('values', [])

            while values != []:
                for book in values:
                    if book != []:
                        history.append(book)

                rangeStart += fetchNum
                rangeStr = getA1Notation(self.infoSpreadNames[2], 1, rangeStart, self.historySheetWidth, (rangeStart + fetchNum - 1))

                request = self.sheets_service.spreadsheets().values().get(
                    majorDimension='ROWS', spreadsheetId=userSheetId, range=rangeStr)
                result = try_request_n_retries(request, retryGet)
                values = result.get('values', [])

            self.history = history

        return self.history

    def createUser(self, userName, userEmail, shouldPrint=True):
        '''Creates all the data entries for a new user.'''

        existingUserNames = self.getUserNames()

        if userName in existingUserNames:
            if shouldPrint:
                print('User already exists.')
            return False

        userform_function = {"function": "makeBooksForm", "parameters": [self.service_email, userName]}
        userform_request = self.appsscript_service.scripts().run(body=userform_function,scriptId=self.script_id)
        userform_response = try_request_n_retries(userform_request, 5)

        userform_dict = userform_response['response'].get('result', {})
        userform_link = userform_dict['form_url']
        userform_id = userform_dict['form_id']

        user_record = [userName, userEmail, userform_link, userform_id]

        newRecordNumber = len(existingUserNames) + 1
        rangeStr = getA1Notation(self.infoSpreadNames[1], 1, newRecordNumber, self.userSheetWidth, newRecordNumber)
        sheetId = self.getBookClubInfoSheetID()
        update_body = {
            "range": rangeStr,
            "majorDimension": "ROWS",
            "values": [user_record],
        }
        update_request = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheetId, range=rangeStr, valueInputOption='RAW', body=update_body)

        update_response = try_request_n_retries(update_request, 5)

        self.userTable[userName] = user_record

        return books_common.User(userName, userEmail, [], userform_link)

    def removeBook(self, book):
        '''Deletes a book from a user's remote list.'''

        loc = book.location
        if not isinstance(loc, FormLocation):
            raise TypeError('Provided book has an incompatible location type.')

        formId = loc.formId
        responseId = loc.responseId

        delbook_function = {"function": "delResponse", "parameters": [formId, responseId]}
        delbook_request = self.appsscript_service.scripts().run(body=delbook_function,scriptId=self.script_id)
        delbook_response = try_request_n_retries(delbook_request, 5)

        return True

    def addWinner(self, book):
        '''Adds a winner to the history file.'''

        history = self.getHistory()
        date = time.strftime('%Y/%m/%d')

        winner_record = [date, book.getTitle(), book.getAuthorFName(), book.getAuthorLName()]

        newRecordNumber = len(history) + 1
        rangeStr = getA1Notation(self.infoSpreadNames[2], 1, newRecordNumber, self.historySheetWidth, newRecordNumber)
        sheetId = self.getBookClubInfoSheetID()
        update_body = {
            "range": rangeStr,
            "majorDimension": "ROWS",
            "values": [winner_record],
        }
        update_request = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheetId, range=rangeStr, valueInputOption='RAW', body=update_body)

        update_response = try_request_n_retries(update_request, 5)

        self.history.append(winner_record)

    def getCurrentPoll(self, retryGet=5):
        '''Returns the currently ongoing book poll.'''

        userSheetId = self.getBookClubInfoSheetID()
        
        rangeStr = getA1Notation(self.infoSpreadNames[3], self.pollIdPos[0], self.pollIdPos[1], self.pollIdPos[0], self.pollIdPos[1])
        request = self.sheets_service.spreadsheets().values().get(
            majorDimension='ROWS', spreadsheetId=userSheetId, range=rangeStr)
        result = try_request_n_retries(request, retryGet)
        values = result.get('values', [])

        currentPollId = ''
        if values and values[0] and values[0][0]:
            currentPollId = values[0][0]

        if currentPollId == '':
            return None

        getpoll_function = {"function": "getPollInfo", "parameters": [currentPollId]}
        getpoll_request = self.appsscript_service.scripts().run(body=getpoll_function,scriptId=self.script_id)
        getpoll_response = try_request_n_retries(getpoll_request, 5)

        pollDict = getpoll_response.['response'].get('result', {})
        
        options = []
        scores = []
        for i in range(len(pollDict['options'])):
            title, author = pollDict['options'][i].split(' by ', maxsplit=1)
            first, last = author.split(maxsplit=1)

            options.append(books_common.Book(title, first, last, None, self))
            scores.append(int(pollDict['scores'][i]))

        formLink = pollDict['url']

        dateCreated = books_common.Date(int(pollDict['date']['year']),
                                        int(pollDict['date']['month']),
                                        int(pollDict['date']['day']))

        return books_common.Poll(options, scores, formLink, dateCreated, self)

    def newPoll(self, poll):
        raise NotImplementedError('Abstract method "newPoll" not implemented')

    def closePoll(self, poll):
        raise NotImplementedError('Abstract method "closePoll" not implemented')
