from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from user_config_control import UserConfig
import logging

s_logger = logging.getLogger(__name__)
s_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

s_file_handler = logging.FileHandler('logs/google_api.log')
s_file_handler.setFormatter(formatter)

s_logger.addHandler(s_file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

s_logger.addHandler(stream_handler)


class GoogleSheetsControl:

    def __init__(self, creds, user: UserConfig):
        self.creds = creds
        self.user = user

        try:
            s_logger.info("Building service for google sheets")
            service = build('sheets', 'v4', credentials=creds)
            # Call the Sheets API
            self.sheet = service.spreadsheets()
        except HttpError as err:
            s_logger.exception(err)

    def get_sheet(self) -> list:
        s_logger.info("Getting value for logger")
        try:
            # Gets values of spreadsheet
            result = self.sheet.values().get(spreadsheetId=self.user.get_google_sheet_link(),
                                             range=self.user.get_sheet_range()).execute()
            values = result.get('values', [])
            return values
        except HttpError as err:
            s_logger.exception(err)

