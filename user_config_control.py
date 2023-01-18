import keyring
import re
import json


class UserConfig:

    def __init__(self, user_config: dict, service_id: str):

        self.receiver = user_config['receiver']
        self.sender = user_config['sender']
        self.service_id = service_id
        self.credentials_file = user_config['credentials_file_name']
        self.notify_time = self._parse_time(user_config['notify_time'])

        # set password
        self._set_password()

    def _set_password(self):
        app_password = input(f"Input APP PASSWORD for account {self.sender}: ")
        # Encrypt password
        keyring.set_password(self.service_id, username=self.sender, password=app_password)

    def get_password(self):
        password = keyring.get_password(self.service_id, self.sender)
        print(f"The passowrd received is: {password}")
        return password

    def get_receiver(self):
        return self.receiver

    def get_sender(self):
        return self.sender

    def get_notify_time(self):
        return self.notify_time

    def get_credentials_file(self):
        return self.credentials_file

    @staticmethod
    def parse_config(config_file_name) -> dict:
        try:
            file = open(config_file_name)
        except OSError:
            print(OSError)

        with file:
            file_info = json.load(file)

        return file_info

    @staticmethod
    def _parse_time(time):
        if re.match("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", time):
            print("In correct format")
            # In proper time
            return time
        else:
            # If not in proper time, will notify at 12AM (midnight)
            return "00:00"
