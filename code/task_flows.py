'''A collection of functions that perform various book club tasks.'''

import books_common
import google_api

def book_club_exist(g_api):
    '''Checks if there is a book club already.'''
    try:
        sheet_id = g_api.get_book_club_info_sheet_id()
    except google_api.SpreadsheetFormatError:
        return False
    else:
        return True

def create_new_book_club(g_api):
    '''Creates the basic infrastructure for a book club.'''
    try:
        result = g_api.make_new_book_club()
    except (google_api.errors.HttpError, google_api.AppsScriptError):
        return False

    return result

def create_poll(g_api, n=4):
    '''Creates a new poll with n options.'''
    pass

def end_poll(g_api):
    '''Ends the current poll and selects a winner.'''
    pass

def create_new_user(g_api, username, user_email):
    '''Creates the infrastructure for a new user.'''
    pass

def delete_user(g_api, username):
    '''Deletes all record of user.'''
    pass

def delete_user_book(g_api, user, book_index):
    '''Deletes the book at user.books[book_index]'''
    pass
