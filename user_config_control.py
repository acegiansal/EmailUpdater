import keyring
import re
import json
import logging

u_logger = logging.getLogger(__name__)
u_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

u_file_handler = logging.FileHandler('logs/email_updater.log')
u_file_handler.setFormatter(formatter)

u_logger.addHandler(u_file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

u_logger.addHandler(stream_handler)


class UserConfig:

    def __init__(self, user_config: dict, service_id: str):

        self.receiver = user_config['receiver']
        self.sender = user_config['sender']
        self.service_id = service_id
        self.credentials_file = user_config['credentials_file_name']
        self.google_sheet_link = user_config['google_sheet_link']
        self.sheet_range = user_config['sheet_range']
        self.notify_time = self._parse_time(user_config['notify_time'])
        self.sheet_type = user_config['sheet_type']

        # set password
        self._set_password()

    def _set_password(self):
        app_password = input(f"Input APP PASSWORD for account {self.sender}: ")
        # Encrypt password
        keyring.set_password(self.service_id, username=self.sender, password=app_password)

    def get_password(self):
        password = keyring.get_password(self.service_id, self.sender)
        return password

    def get_receiver(self):
        return self.receiver

    def get_sender(self):
        return self.sender

    def get_notify_time(self):
        return self.notify_time

    def get_credentials_file(self):
        return self.credentials_file

    def get_google_sheet_link(self):
        return self.google_sheet_link

    def get_sheet_range(self):
        return self.sheet_range

    def get_sheet_type(self):
        return self.sheet_type

    @staticmethod
    def parse_config(config_file_name) -> dict:
        try:
            file = open(config_file_name)
        except OSError:
            u_logger.exception(OSError)

        with file:
            file_info = json.load(file)

        return file_info

    @staticmethod
    def _parse_time(time):
        if re.match("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", time):
            u_logger.info(f"Time set to {time}")
            return time
        else:
            u_logger.warning("Time not in valid format (expected [##:##]). Setting to midnight")
            # If not in proper time, will notify at 12AM (midnight)
            return "00:00"
