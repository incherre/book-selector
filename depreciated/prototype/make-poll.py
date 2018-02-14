import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

#-----Function Declarations-----
def get_yn(prompt): # a method for getting a yes/no answer
    yn = False
    answer = ''

    while not yn:
        answer = input(prompt)
        if answer.lower()[0] == 'y':
            yn = True
            return True
        elif answer.lower()[0] == 'n':
            yn = True
            return False
        else:
            print("Please respond with y/es or n/o.")

def get_and_confirm(prompt): # a method for getting input and confirming the user has entered it correctly
    item = input(prompt)
    confirmed = False

    while not confirmed:
        temp_answer = get_yn("Is '" + item + "' correct? (y/n) ")
        if temp_answer:
            confirmed = True
        else:
            item = input(prompt)

    return item

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
        return book

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

#-----Script Start-----
poll_number = 4

scope =  [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive'
]

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name('book-selector-key.json', scope)
    gc = gspread.authorize(credentials)
except:
    print("Error: failed to authenticate")
    exit()

sheet_name = get_and_confirm("Please enter the name of the book club: ")

try:
    sh = gc.open(sheet_name)
except:
    print("Error: sheet not opened.")
    exit()

worksheet_list = sh.worksheets()

user_worksheets = get_user_worksheets(worksheet_list)

print("Getting Books...")
finalist_books = select_n_books(user_worksheets, poll_number)

print("Books to be voted on:")
for book in finalist_books:
    print(book[2] + ': ' + book[0] + " by " + book[1])

print("\nAdding books to vote sheet...")
try:
    vote = sh.worksheet("CurrentVote")
    vote.clear()
    vote.insert_row(["Votes", "Titles", "Authors", "", "Suggester", "Reserved, DNE"], 1)
except:
    print("Error: sheet not opened.")
    exit()

index = 2
for book in finalist_books:
    row_book = [0] + book[:2] + [''] + book[2:]
    try:
        vote.insert_row(row_book, index)
    except:
        print("Error: '" + book[0] + "' not added correctly.")
    index += 1

print("Done.")
