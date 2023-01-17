from __future__ import print_function

import smtplib
import ssl

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

TEST_EMAIL = "giandevmail@gmail.com"
TEST_PASSWORD = 'edaayvzexfwintzr'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    file_name = 'token.json'
    if os.path.exists(file_name):
        print("Found token")
        creds = Credentials.from_authorized_user_file(file_name, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        ########################## Start of Gian Code

        # Read Spreadsheet
        # spreadsheet_name = "Assignment tracker"
        # sheet = SpreadSheetCom.open_spreadsheet(spreadsheet_name)
        # range = "B3:G16"
        # print(SpreadSheetCom.get_range_values(range))

        # Send email
        PORT = 465

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
            server.login(TEST_EMAIL, TEST_PASSWORD)
            target_email = "acegiansal@gmail.com"
            message = """
            Subject: Test

            Hello there, this is a test from python
            """
            server.sendmail(TEST_EMAIL, target_email, message)


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()