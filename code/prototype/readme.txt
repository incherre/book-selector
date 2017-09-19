Book-Selector prototype
Daniel Fitzick

These scripts rely on gspread, oauth2client, and PyOpenSSL. Please make sure these are installed before using.
Also these scripts require Google OAuth credentials. Please store these credentials in a file called
'book-selector-key.json' in the same directory as the scripts.
All scripts are written for Python 3.

To create a new book club spreadsheet:
-Run 'setup-sheet.py'
-Enter a sheet name. This name is used with the other scripts later.
-Enter user email addresses. Make sure to enter at least one that you control so you can have access to the spreadsheet.

To create a poll:
-Run 'make-poll.py'
-Enter your sheet name.

To select winners for a poll:
-Run 'end-poll.py'
-Enter your sheet name.

To add a new user:
-Go to the spreadsheet in your browser
-Add a new worksheet
-Change the title of the new worksheet to the user's username
-Invite that user to the spreadsheet with the ability to edit

Notes:
-User's worksheets should have one book per row with the title in the first column and the author in the second.
-Only books from row one until the first blank row will be considered.
-Vote counts can be freely edited by all members, make sure you trust them.