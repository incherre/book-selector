import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import datetime

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
    hist = sh.worksheet("History")
    vote = sh.worksheet("CurrentVote")
except:
    print("Error: failed to open sheet")
    exit()

votes = vote.range(2, 1, poll_number + 1, 1)

winners = []
for cell in votes:
    try:
        val = int(cell.value)
    except:
        print("Error: malformed vote")
        exit()
    
    if not winners: #checking if winners is empty
        winners = [cell]
    elif val == int(winners[0].value):
        winners.append(cell)
    elif val > int(winners[0].value):
        winners = [cell]

if len(winners) > 1:
    print("There was a tie! Using a random tie-breaker.")

final_winner = random.choice(winners)
winner_index = final_winner.row

try:
    winner_entry = vote.row_values(winner_index)[:6]
except:
    print("Error: failed to retrieve winner record")
    exit()

print("The winner is " + winner_entry[1] + " by " + winner_entry[2] + "!")

print("Adding winner to history...")
today = datetime.datetime.now().strftime("%B %d, %Y")
win_fields = [today] + winner_entry[1:3] + [winner_entry[4]]

try:
    hist.insert_row(win_fields, 2)
except:
    print("Error: failed to record winner")
    exit()

print("Removing winner from origin list...")
try:
    origin = sh.worksheet(winner_entry[4])
    origin.delete_row(int(winner_entry[5]))
except:
    print("Error: failed to delete winner")

print("Clearing Poll...")
try:
    vote.clear()
except:
    print("Error: failed to clear poll")

print("Done.")
