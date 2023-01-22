import schedule
import time
from user_config_control import UserConfig
from google_api.google_api_control import GoogleApiControl
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

# MAIN CODE
if __name__ == "__main__":
    """
    DO 1 AND 2 IN A LOOP FOR ALL USERS IN CONFIG FILE
    1. Get user information (all from file but sender app password, which will be asked for)
        - receiver email
        - Sender email
        - Sender app password
        - Time to alert
        - Google sheet link
    2. Get google credentials
    ----------
    3. Schedule assignment
    4. Await scheduled tasks
    """
    config_file_name = "userconfig.json"
    config_dict = UserConfig.parse_config(config_file_name)

    for user_config in config_dict['users']:
        user = UserConfig(user_config, config_dict['service_id'])
        api_control = GoogleApiControl(user)

        u_logger.info(f"Scheduling check/notify for {user.get_notify_time()}")

        schedule.every().day.at(user.get_notify_time()).do(api_control.check_sheet)

    while True:
        u_logger.info("Checking for scheduled run at time ")
        schedule.run_pending()
        # Wait every 30 minutes before checking
        time.sleep(1800)
