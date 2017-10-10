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

#-----Script Start-----
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
    sh = gc.create(sheet_name)
    sh.add_worksheet("History", 100, 4)
    sh.add_worksheet("CurrentVote", 100, 6)
    
    sh2 = gc.open(sheet_name) #the first instance never shows 'sheet1'
    sh2.del_worksheet(sh2.sheet1)
except BaseException as e:
    print(e)
    print("Error: failed to create sheet")
    exit()
else:
    print("Created sheet.")

print("\nCreating users.")
leave = False
while not leave:
    email = get_and_confirm("Please enter next user's email: ")
    uname = email.split('@')[0]
    try:
        sh.add_worksheet(uname, 100, 2)
        sh.share(email, perm_type='user', role='writer')
    except:
        print("Error: failed to create user")
    else:
        print("Created user.")

    leave = not get_yn("Would you like to enter another user? (y/n) ")
