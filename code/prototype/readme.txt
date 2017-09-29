Book-Selector prototype
Daniel Fitzick

These scripts rely on the libraries gspread, oauth2client, and PyOpenSSL. Please make sure these are installed before using. These scripts also require Google OAuth credentials. Please store these credentials in a file called 'book-selector-key.json' in the same directory as the scripts. Here is a tutorial for setting this up: http://gspread.readthedocs.io/en/latest/oauth2.html Heads up: some of the exact steps in obtaining the Google Oauth token are out of date. Here is an install guide for gspread itself: https://github.com/burnash/gspread/blob/master/README.md I used the "from github" installation method and ran the install script with Python 3.
All scripts are written for Python 3.

This is designed as a set of scripts that an admin runs to operate a bookclub. All user interaction is done through a shared Google Sheets document, so no personal hosting is required.

As the admin:
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

As the user:
To add a book to your list:
-Go to the spreadsheet in your browser (you should have recieved an invite link)
-Navigate to your worksheet
-Add a new line
-Enter the book title into the first cell in the new line
-Enter the book's author into the second cell in the new line

To vote:
-Go to the spreadsheet in your browser (you should have recieved an invite link)
-Navigate to the "CurrentVote" worksheet
-Decide on your favorite option
-Edit the "votes" column for your favorite option to be one more than it was before

To view past and current winners:
-Go to the spreadsheet in your browser (you should have recieved an invite link)
-Navigate to the "History" worksheet

Notes:
-User's worksheets should have one book per row with the title in the first column and the author in the second.
-Only books from row one until the first blank row will be considered.
-Vote counts can be freely edited by all members, make sure you trust them.
