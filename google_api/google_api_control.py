from __future__ import print_function

import logging

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from user_config_control import UserConfig
from google_api.google_sheets_control import GoogleSheetsControl
from google_api.gmail_control import GmailControl
from google_api.sheet_readers.sheet_reader_control import SheetReaderContext

g_logger = logging.getLogger(__name__)
g_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

g_file_handler = logging.FileHandler('logs/google_api.log')
g_file_handler.setFormatter(formatter)

g_logger.addHandler(g_file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

g_logger.addHandler(stream_handler)


class GoogleApiControl:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, user: UserConfig):
        self.user = user
        self.creds = self.create_creds(self.user.get_credentials_file())
        self.gmail_ctr = GmailControl(self.user)
        self.sheets_ctr = GoogleSheetsControl(self.creds, self.user)
        self.sheet_reader = SheetReaderContext.determine_reader(self.user.get_sheet_type())
        g_logger.info("Finished creating GoogleApiControl")

    def reset_creds(self):
        self.creds = self.create_creds(self.user.get_credentials_file())

    def create_creds(self, credentials_file):
        creds = None

        token_name = f"token.{credentials_file}"

        g_logger.info(f"Creating file {token_name} for credentials")

        ###### NOTE: Below code is taken from google quick start for google sheets API #####

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_name):
            creds = Credentials.from_authorized_user_file(token_name, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_name, 'w') as token:
                token.write(creds.to_json())
        return creds

    def check_sheet(self):
        sheet_info = self.sheets_ctr.get_sheet()
        message = {"lines": []}
        notify_counter = 0
        row_counter = 0
        for row in sheet_info:
            g_logger.info(f" Row {row_counter} ----------------")
            if self.sheet_reader.should_notify_user(row):
                notify_counter += 1
                if message.get('Subject') is None:
                    message['Subject'] = self.sheet_reader.get_subject()
                if message.get('links') is None:
                    message['links'] = self.sheet_reader.get_links()
                message["lines"] += self.sheet_reader.create_message(row)
            row_counter += 1
        g_logger.info(f"Finished reading. Read {row_counter} rows")

        if len(message['lines']) > 0:
            message['title'] = self.sheet_reader.get_title(notify_counter)
            # If a subject was created, the user should be notified
            self._notify_user(message)
        else:
            g_logger.info("Notifying user not required")

    def _notify_user(self, message):
        g_logger.info("Notifying user")
        self.gmail_ctr.send_email(message)
