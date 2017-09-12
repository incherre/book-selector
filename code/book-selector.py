import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

scope =  [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('book-selector-key.json', scope)

gc = gspread.authorize(credentials)

#sh = gc.create('BookClubTest')
#sh.share('user@domain.com', perm_type='user', role='writer')

sh = gc.open('BookClubTest')

worksheet_list = sh.worksheets()

def get_user_worksheets(all_worksheets):
    reserved_names = set()
    reserved_names.add('History')
    reserved_names.add('CurrentVote')
    
    user_worksheets = []
    for worksheet in all_worksheets:
        if not worksheet.title in reserved_names:
            user_worksheets.append(worksheet)
            
    return user_worksheets

def get_book_count(worksheet): #O(n)  :(
    col = worksheet.col_values(1)
    return col.index('')

def select_random_book(worksheet):
    num_books = get_book_count(worksheet)
    
    if num_books < 1:
        print('Error: too few books in list "' + worksheet.title + '"')
        return None
    else:
        row = random.randint(1, num_books)
        book = worksheet.row_values(row)[:2] + [worksheet.title, row]
        return book #TODO: make a book object...

def select_n_books(user_worksheets, n):
    if len(user_worksheets) < n:
        print('Error: too few users!')
        return None
    else:
        books = []
        lucky_users = random.sample(user_worksheets, n)
        for user in lucky_users:
            books.append(select_random_book(user))
        return books

user_worksheets = get_user_worksheets(worksheet_list)

print("Books to be voted on:")
finalist_books = select_n_books(user_worksheets, 4)
for book in finalist_books:
    print(book[2] + ': ' + book[0] + " by " + book[1])
