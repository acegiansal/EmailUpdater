from googleapiclient.discovery import build
from user_config_control import UserConfig


class GoogleSheetsControl:

    def __init__(self, creds, user: UserConfig):
        self.creds = creds
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=user.get_google_sheet_link(),
                                    range=user.get_sheet_range()).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[5]))
