import os
import time
import string

import httplib2

from apiclient import discovery
from apiclient import errors

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools

import books_common

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
    '''Tries a request up to some number of times. Only retries on failure.'''

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

def column_number_to_letter(column_number):
    '''Converts a column number to the column letters used by the Google apis.'''

    column_letter = ''
    unconverted_part = column_number
    while unconverted_part > 0:
        letter_index = (unconverted_part - 1) % 26
        column_letter = string.ascii_uppercase[letter_index] + column_letter
        unconverted_part = int((unconverted_part - letter_index - 1) / 26)
    return column_letter

def get_a1_notation(sheet_name, col1, row1, col2, row2):
    '''Converts coordinates to the appropriate notation.'''

    a1_notation = "'" + sheet_name + "'!"
    a1_notation += column_number_to_letter(col1) + str(row1) + ':'
    a1_notation += column_number_to_letter(col2) + str(row2)
    return a1_notation

class AppsScriptError(Exception):
    pass

class SpreadsheetFormatError(Exception):
    pass

class FormLocation(books_common.Location):
    '''A class representing where a book is stored when used with GoogleDocsBot.'''

    def __init__(self, form_id, response_id):
        if isinstance(form_id, str):
            self.form_id = form_id
        else:
            raise TypeError("Provided form ID not a string.")

        if isinstance(response_id, str):
            self.response_id = response_id
        else:
            raise TypeError("Provided response ID not a string.")

    def get_form_id(self):
        '''Returns the form id.'''

        return self.form_id

    def get_response_id(self):
        '''Returns the response id.'''

        return self.response_id

    def compare(self, other):
        same = True
        same = same and isinstance(other, FormLocation)
        same = same and self.form_id == other.form_id
        same = same and self.response_id == other.response_id
        return same

class GoogleDocsBot(books_common.DataIO):
    '''A class representing the functions to communicate with Google Drive.'''

    service_scope = ['https://www.googleapis.com/auth/drive',
                     'https://www.googleapis.com/auth/spreadsheets']

    appsscript_scope = ['https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/forms',
                        'https://www.googleapis.com/auth/userinfo.email']

    info_spread_names = ('BookClubInfo', 'Users', 'History', 'GlobalInfo')
    user_sheet_width = 4
    history_sheet_width = 4
    poll_id_position = (1, 1)
    location_width = 3

    max_retries = 5
    fetch_number = 10

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
            # create service account api services
            service_creds = ServiceAccountCredentials.from_json_keyfile_name(credential_path, self.service_scope)
            drive_http = service_creds.authorize(httplib2.Http())
            self.drive_service = discovery.build('drive', 'v3', http=drive_http)
            self.sheets_service = discovery.build('sheets', 'v4', credentials=service_creds)

            # get the service account's email for sharing
            self.service_email = service_creds._service_account_email
        except FileNotFoundError:
            print('File: "' + str(credential_path) + '" was not found.')
            raise

        try:
            # get the user's credentials and build the apps script service
            appsscript_creds = get_credentials(credential_name, client_secret_path, self.appsscript_scope, app_name)
            appsscript_http = appsscript_creds.authorize(httplib2.Http())
            self.appsscript_service = discovery.build('script', 'v1', http=appsscript_http)

            # get the user's email for transferring ownership
            email_function = {"function": "getEmail", "parameters": []}
            email_request = self.appsscript_service.scripts().run(body=email_function, scriptId=self.script_id)
            email_response = try_request_n_retries(email_request, self.max_retries)
            self.admin_email = email_response['response'].get('result', str)

            if self.admin_email == '':
                raise AppsScriptError('Failed to retrieve user email.')

        except FileNotFoundError:
            print('File: "' + str(client_secret_path) + '" was not found.')
            raise

    def get_file_list(self):
        '''Returns a list of files accessible by the service account.'''

        files_request = self.drive_service.files().list(fields="nextPageToken, files(id, name)")
        files_results = try_request_n_retries(files_request, self.max_retries)
        files = files_results.get('files', [])
        next_page_token = files_results.get('nextPageToken')

        while next_page_token and next_page_token != '':
            #make sure to get the full list if required
            files_request = drive_service.files().list(pageToken=next_page_token,
                                                       fields="nextPageToken, files(id, name)")
            files_results = try_request_n_retries(files_request, self.max_retries)
            files += files_results.get('files', [])
            next_page_token = files_results.get('nextPageToken')

        return files

    def get_book_club_info_sheet_id(self):
        '''Returns the file id of the sheet used to store book club information.'''

        if not hasattr(self, 'book_club_info_sheet_id'):
            files = self.get_file_list()
            self.book_club_info_sheet_id = None
            if files:
                for item in files:
                    if item['name'] == self.info_spread_names[0]:
                        self.book_club_info_sheet_id = item['id']

            if not self.book_club_info_sheet_id:
                del self.book_club_info_sheet_id
                raise SpreadsheetFormatError('No User spreadsheet found.')

        return self.book_club_info_sheet_id

    def get_user_table(self):
        '''Returns a matrix of user records.'''

        if not hasattr(self, 'user_table'):
            user_sheet_id = self.get_book_club_info_sheet_id()

            range_start = 1
            user_info = {}

            range_string = get_a1_notation(self.info_spread_names[1], 1, range_start, self.user_sheet_width, (range_start + self.fetch_number - 1))
            users_request = self.sheets_service.spreadsheets().values().get(
                majorDimension='ROWS', spreadsheetId=user_sheet_id, range=range_string)
            users_result = try_request_n_retries(users_request, self.max_retries)
            values = users_result.get('values', [])

            while values != []:
                for user in values:
                    if user != []:
                        user_info[user[0]] = user

                range_start += self.fetch_number
                range_string = get_a1_notation(self.info_spread_names[1], 1, range_start, self.user_sheet_width, (range_start + self.fetch_number - 1))

                users_request = self.sheets_service.spreadsheets().values().get(
                    majorDimension='ROWS', spreadsheetId=user_sheet_id, range=range_string)
                users_result = try_request_n_retries(users_request, self.max_retries)
                values = users_result.get('values', [])

            self.user_table = user_info

        return self.user_table

    def make_new_book_club(self, should_print=True):
        '''Creates the document structure for a new book club. Returns success.'''

        #start checking for old book club code
        files = self.get_file_list()
        if files:
            for item in files:
                if item['name'] == self.info_spread_names[0]:
                    if should_print:
                        print('Book Club already exists under this bot.')
                    return False #Can't make a new book club when there is already one
        #end checking for old book club code

        #start creating new book club code
        spreadsheet_body = {
            "properties": {
                "title": self.info_spread_names[0]
            },
            "sheets": [
                {
                    "properties": {
                        "title": self.info_spread_names[1],
                        "index": 0
                    }
                },
                {
                    "properties": {
                        "title": self.info_spread_names[2],
                        "index": 1
                    }
                }
            ]
        }
        new_sheet_request = self.sheets_service.spreadsheets().create(body=spreadsheet_body)
        try:
            new_sheet_response = try_request_n_retries(new_sheet_request, self.max_retries) #make the new spreadsheet
        except errors.HttpError:
            if should_print:
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

        share_response = try_request_n_retries(share_request, self.max_retries) #share the new spreadsheet
        #end sharing code

        return True

    def get_user_names(self):
        '''Returns a list of usernames.'''

        user_table = self.get_user_table()

        user_names = list(user_table.keys())

        return user_names

    def get_user_info(self, username):
        '''Returns a user's information.'''

        user_info = []
        user_table = self.get_user_table()

        if username in user_table:
            user_info = user_table[username]

        if len(user_info) >= self.user_sheet_width:
            return books_common.User(user_info[0], user_info[1], [], user_info[2])

        return user_info

    def get_user_books(self, user):
        '''Returns the list of books entered by the user and updates the user object's book list.'''

        username = user.get_user_name()
        get_form_id = None
        user_table = self.get_user_table()

        if username in user_table:
            get_form_id = user_table[username][3]
        else:
            raise SpreadsheetFormatError('Requested User does not exist.')

        getbooks_function = {"function": "getBookList", "parameters": [get_form_id]}
        getbooks_request = self.appsscript_service.scripts().run(body=getbooks_function, scriptId=self.script_id)
        getbooks_response = try_request_n_retries(getbooks_request, self.max_retries)

        rawbooks_list = getbooks_response['response'].get('result', [])
        books_list = [books_common.Book(i['title'], i['authorFirstName'], i['authorLastName'],
                                        FormLocation(get_form_id, i['formResponseId']), self)
                      for i in rawbooks_list]

        user.replace_books(books_list)

        return books_list

    def get_history(self):
        '''Gets a list of books that have previously won a contest.'''

        if not hasattr(self, 'history'):
            user_sheet_id = self.get_book_club_info_sheet_id()

            range_start = 1
            history = []

            range_string = get_a1_notation(self.info_spread_names[2], 1, range_start, self.history_sheet_width, (range_start + self.fetch_number - 1))
            history_request = self.sheets_service.spreadsheets().values().get(
                majorDimension='ROWS', spreadsheetId=user_sheet_id, range=range_string)
            history_result = try_request_n_retries(history_request, self.max_retries)
            values = history_result.get('values', [])

            while values != []:
                for book in values:
                    if book != []:
                        history.append(book)

                range_start += self.fetch_number
                range_string = get_a1_notation(self.info_spread_names[2], 1, range_start, self.history_sheet_width, (range_start + self.fetch_number - 1))

                history_request = self.sheets_service.spreadsheets().values().get(
                    majorDimension='ROWS', spreadsheetId=user_sheet_id, range=range_string)
                history_result = try_request_n_retries(history_request, self.max_retries)
                values = history_result.get('values', [])

            self.history = history

        return self.history

    def create_user(self, username, user_email, should_print=True):
        '''Creates all the data entries for a new user.'''

        existing_user_names = self.get_user_names()

        if username in existing_user_names:
            if should_print:
                print('User already exists.')
            return False

        userform_function = {"function": "makeBooksForm", "parameters": [self.service_email, username]}
        userform_request = self.appsscript_service.scripts().run(body=userform_function, scriptId=self.script_id)
        userform_response = try_request_n_retries(userform_request, self.max_retries)

        userform_dict = userform_response['response'].get('result', {})
        userform_link = userform_dict['form_url']
        userform_id = userform_dict['form_id']

        user_record = [username, user_email, userform_link, userform_id]

        new_record_number = len(existing_user_names) + 1
        range_string = get_a1_notation(self.info_spread_names[1], 1, new_record_number, self.user_sheet_width, new_record_number)
        user_sheet_id = self.get_book_club_info_sheet_id()
        update_body = {
            "range": range_string,
            "majorDimension": "ROWS",
            "values": [user_record],
        }
        update_request = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=user_sheet_id, range=range_string, valueInputOption='RAW', body=update_body)

        update_response = try_request_n_retries(update_request, self.max_retries)

        self.user_table[username] = user_record

        return books_common.User(username, user_email, [], userform_link)

    def remove_book(self, book):
        '''Deletes a book from a user's remote list.'''

        loc = book.location
        if not isinstance(loc, FormLocation):
            raise TypeError('Provided book has an incompatible location type.')

        form_id = loc.get_form_id()
        response_id = loc.get_response_id()

        delbook_function = {"function": "delResponse", "parameters": [form_id, response_id]}
        delbook_request = self.appsscript_service.scripts().run(body=delbook_function, scriptId=self.script_id)
        delbook_response = try_request_n_retries(delbook_request, self.max_retries)

        return True

    def add_winner(self, book):
        '''Adds a winner to the history file.'''

        history = self.get_history()
        date = time.strftime('%Y/%m/%d')

        winner_record = [date, book.get_title(), book.get_author_first_name(), book.get_author_last_name()]

        new_record_number = len(history) + 1
        range_string = get_a1_notation(self.info_spread_names[2], 1, new_record_number, self.history_sheet_width, new_record_number)
        user_sheet_id = self.get_book_club_info_sheet_id()
        update_body = {
            "range": range_string,
            "majorDimension": "ROWS",
            "values": [winner_record],
        }
        update_request = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=user_sheet_id, range=range_string, valueInputOption='RAW', body=update_body)

        update_response = try_request_n_retries(update_request, self.max_retries)

        self.history.append(winner_record)

    def get_current_poll(self):
        '''Returns the currently ongoing book poll.'''

        user_sheet_id = self.get_book_club_info_sheet_id()

        range_string = get_a1_notation(self.info_spread_names[3], self.poll_id_position[0], self.poll_id_position[1], self.poll_id_position[0], self.poll_id_position[1])
        request = self.sheets_service.spreadsheets().values().get(
            majorDimension='ROWS', spreadsheetId=user_sheet_id, range=range_string)
        result = try_request_n_retries(request, self.max_retries)
        values = result.get('values', [])

        current_poll_id = ''
        if values and values[0] and values[0][0]:
            current_poll_id = values[0][0]

        if current_poll_id == '':
            return None

        getpoll_function = {"function": "getPollInfo", "parameters": [current_poll_id]}
        getpoll_request = self.appsscript_service.scripts().run(body=getpoll_function, scriptId=self.script_id)
        getpoll_response = try_request_n_retries(getpoll_request, self.max_retries)

        poll_dict = getpoll_response['response'].get('result', {})

        option_count = len(poll_dict['options'])
        range_string = get_a1_notation(self.info_spread_names[3], self.poll_id_position[0], self.poll_id_position[1] + 1, self.location_width, option_count + 1)
        location_request = self.sheets_service.spreadsheets().values().get(
            majorDimension='ROWS', spreadsheetId=user_sheet_id, range=range_string)
        location_result = try_request_n_retries(location_request, self.max_retries)
        values = location_result.get('values', [])

        location_dict = {}
        for row in values:
            location_dict[row[0]] = FormLocation(row[1], row[2])

        options = []
        scores = []
        for i in range(option_count):
            id_string = poll_dict['options'][i]
            title, author = id_string.split(': ', maxsplit=1)
            last, first = author.split(', ', maxsplit=1)

            options.append(books_common.Book(title, first, last, location_dict[id_string], self))
            scores.append(int(poll_dict['scores'][i]))

        form_link = poll_dict['url']

        date_created = books_common.Date(int(poll_dict['date']['year']),
                                         int(poll_dict['date']['month']),
                                         int(poll_dict['date']['day']))

        return books_common.Poll(options, scores, form_link, current_poll_id, date_created, self)

    def new_poll(self, options):
        '''Replaces the old poll with the provided poll. close_poll should often be called on the old poll first.'''

        string_options = []
        location_data = []
        for i in options:
            identifier = i.get_title() + ': ' + i.get_author_last_name() + ', ' + i.get_author_first_name()
            string_options.append(identifier)

            loc = i.location
            location_data.append([identifier, loc.get_form_id(), loc.get_response_id()])

        makepoll_function = {"function": "makePollForm", "parameters": [self.service_email, string_options]}
        makepoll_request = self.appsscript_service.scripts().run(body=makepoll_function, scriptId=self.script_id)
        makepoll_response = try_request_n_retries(makepoll_request, self.max_retries)

        pollform_dict = makepoll_response['response'].get('result', {})
        pollform_link = pollform_dict['form_url']
        pollform_id = pollform_dict['form_id']

        range_string = get_a1_notation(self.info_spread_names[3], self.poll_id_position[0], self.poll_id_position[1], self.location_width, len(location_data) + 1)
        user_sheet_id = self.get_book_club_info_sheet_id()
        update_body = {
            "range": range_string,
            "majorDimension": "ROWS",
            "values": [[pollform_id]] + location_data,
        }
        update_request = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=user_sheet_id, range=range_string, valueInputOption='RAW', body=update_body)
        update_response = try_request_n_retries(update_request, self.max_retries)

        scores = [0] * len(options)

        now = time.localtime()
        date_created = books_common.Date(now.tm_year, now.tm_mon, now.tm_mday)

        return books_common.Poll(options, scores, pollform_link, pollform_id, date_created, self)

    def close_poll(self, poll):
        '''Stops the poll from accepting responses.'''

        poll_id = poll.form_id

        closepoll_function = {"function": "closeForm", "parameters": [poll_id]}
        closepoll_request = self.appsscript_service.scripts().run(body=closepoll_function, scriptId=self.script_id)
        closepoll_response = try_request_n_retries(closepoll_request, self.max_retries)
