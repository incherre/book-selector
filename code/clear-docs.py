'''A script to clear the document space of a service account. Used to reset in between tests.'''

import httplib2

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from google_api import try_request_n_retries

service_scope = ['https://www.googleapis.com/auth/drive']
credential_path = './creds/book-selector-key.json'

service_creds = ServiceAccountCredentials.from_json_keyfile_name(
    credential_path, service_scope)

service_email = service_creds._service_account_email

drive_service = discovery.build(
    'drive', 'v3', http=service_creds.authorize(httplib2.Http()))

files_request = drive_service.files().list(fields="nextPageToken, files(id, name)")
files_results = try_request_n_retries(files_request, 5)
files = files_results.get('files', [])
next_page_token = files_results.get('nextPageToken')

while next_page_token and next_page_token != '':
    #make sure to get the full list if required
    files_request = drive_service.files().list(
        pageToken=next_page_token, fields="nextPageToken, files(id, name)")
    files_results = try_request_n_retries(files_request, self.max_retries)
    files += files_results.get('files', [])
    next_page_token = files_results.get('nextPageToken')

if not files:
    print('No files')

for file in files:
    file_info_request = drive_service.permissions().list(
        fileId=file['id'], fields='permissions(id, emailAddress, role)')
    file_info_results = try_request_n_retries(file_info_request, 5)
    permissions = file_info_results.get('permissions')

    my_permission = None
    for perm in permissions:
        if perm['emailAddress'] == service_email:
            my_permission = perm
            break

    if my_permission['role'] == 'owner':
        print('Deleting ' + file['name'])
        delete_file_request = drive_service.files().delete(fileId=file['id'])
        delete_file_results = try_request_n_retries(delete_file_request, 5)
    else:
        print('Removing own access to ' + file['name'])
        delete_perm_request = drive_service.permissions().delete(
            fileId=file['id'], permissionId=my_permission['id'])
        delete_perm_results = try_request_n_retries(delete_perm_request, 5)

print('Done')
