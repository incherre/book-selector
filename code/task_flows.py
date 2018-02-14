'''A collection of functions that perform various book club tasks.'''

import books_common
import google_api

def create_new_book_club(g_api):
    '''Creates the basic infrastructure for a book club.'''
    try:
        result = g_api.make_new_book_club()
    except (google_api.errors.HttpError, google_api.AppsScriptError):
        return False

    return result

def create_poll(io, n=4):
    '''Creates a new poll with n options.'''
    pass

def end_poll(io):
    '''Ends the current poll and selects a winner.'''
    pass

def create_new_user(io, username, user_email):
    '''Creates the infrastructure for a new user.'''
    pass
