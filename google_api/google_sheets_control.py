from googleapiclient.discovery import build
from user_config_control import UserConfig


class GoogleSheetsControl:

    def __init__(self, creds, user: UserConfig):
        self.creds = creds
        service = build('sheets', 'v4', credentials=creds)

        self.user = user
        # Call the Sheets API
        self.sheet = service.spreadsheets()

    def get_sheet(self) -> list:
        # Gets values of spreadsheet
        result = self.sheet.values().get(spreadsheetId=self.user.get_google_sheet_link(),
                                         range=self.user.get_sheet_range()).execute()
        values = result.get('values', [])

        return values
