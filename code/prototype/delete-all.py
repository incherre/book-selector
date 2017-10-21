import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

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

#WARNING: this script will delete all spreadsheets owned by the credentials used

l = gc.openall()
for spread in l:
    print("deleting: " + spread.title)
    gc.del_spreadsheet(spread.id)
