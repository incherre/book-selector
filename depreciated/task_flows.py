'''A collection of functions that perform various book club tasks.'''

import random
import time

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
    names = g_api.get_user_names()
    p_users = []

    while len(p_users) < n:
        num_to_choose = (n - len(p_users)

        if len(names) < num_to_choose):
            #not enough users (who have books)
            return False

        potentials = random.sample(names, num_to_choose)
        for username in potentials:
            #remove the already selected users
            names.remove(username)

            #build the user structure
            user = g_api.get_user_info(username)
            g_api.get_user_books(user)

            if user.get_num_books() > 0:
                #only add the user if there are books to select
                p_users.append(user)

    books = []
    for user in p_users:
        books.append(random.choice(user.get_books()))

    g_api.new_poll(books)

    return True

def end_poll(g_api):
    '''Ends the current poll and selects a winner.'''
    poll = g_api.get_current_poll()
    poll.close_voting()
    time.sleep(1) #let it settle
    poll.update_results()
    winner = poll.get_winner()
    g_api.add_winner(winner)
    winner.delete() #remove the winner from it's owner's list
    return winner

def create_new_user(g_api, username, user_email):
    '''Creates the infrastructure for a new user.'''
    user = g_api.create_user(username, user_email)
    return user

def delete_user(g_api, username):
    '''Deletes all record of user.'''
    pass

def delete_user_book(g_api, user, book_index):
    '''Deletes the book at user.books[book_index]'''
    book = user.get_books()[book_index]
    book.delete()
