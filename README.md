# book-selector
A project for managing and selecting book recommendations for a book club

## Setup Guide
Note: This application will create Google docs and transfer ownership of them to an admin email account. It will also automatically send emails to users from the admin account. It is recommended that you create a new account specifically for this purpose. It is possible to use an existing email, however it might be annoying to do so.

### Downloading the project
1. Copy book-club.conf, book_club_manager.py, books_common.py, and google_api.py from the project's code folder to a folder on your computer
2. Create a sub-folder named "creds" in the folder you just created

### Creating a new Google API project
General Information: https://developers.google.com/gsuite/marketplace/preparing

1. Navigate to https://console.developers.google.com/cloud-resource-manager
2. Click on "Create Project"
3. Enter as a project name the name of your book club and click create
4. The new project should appear in the list in a minute or so, you may have to refresh
5. Once the new project appears in the list, click on its title
6. On the left hand side click "Service Accounts" and then, in the middle, "Create service account"
7. For the account name enter "Book Club Manager", for the Role select Project>Editor
8. Make sure both check boxes are un-checked and click create
9. Click the menu icon all the way to the right of the newly created service account and click on "create key"
10. Make sure that JSON is selected and click "Create"
11. Save the key file in the creds folder that you created earlier
12. Click the menu icon in the upper left of the project page and select "APIs & Services"
13. Click on "Enable APIs and Services"
14. Search for and enable the Gmail API, the Google Apps Script API, the Google Drive API, and the Google Sheets API
15. Click the menu icon again, navigate to "IAM & admin">Settings and take note of the project number (not the project id or the project name)
16. Navigate to https://script.google.com/home/
17. Click on "New script"
18. Change the title of the new script to the name of your book club
19. Click on "Resources" and select "Cloud Platform Project"
20. Under the "Change Project" heading, enter the project number you noted earlier
21. Click "Set project" and "Confirm", once the project is changed, return to the script
22. Copy the contents of book-selector/code/google-apps-script-target.gs into the new script and save the changes
23. Click on "Publish" and "Deploy as API executable"
24. Enter a new version description and make sure "Anyone" has access to the script
25. Click "Deploy" and take note of the API ID that appears, you'll need it later
26. Navigate back to the new project's dashboard, go to "APIs & Services">Credentials
27. There should be a new OAuth 2.0 client ID named "Apps Script", download the JSON using the button on the right and save it in the creds folder

### Setting up the config file
1. Open your local book-club.conf in a text editor
2. Change the CRED_PATH field to the path of the service account key file that you saved
3. Change the CLINT_SECRET_PATH field to the path of the Apps Script OAuth token you saved
4. Change the APP_NAME field to the name of your book club
5. Change the SCRIPT_ID field to the API ID that you noted earlier
6. Change the OPTION_NUM field to the number of options that you want in the monthly poll

### Installing 
TODO

### First run
1. Use python to run book_club_manager.py
2. It should open your browser to an auth page, make sure you give access to the account that you'd like to be the admin account
3. Wait while the application performs the first time setup
4. The main menu should appear
