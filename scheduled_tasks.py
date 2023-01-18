import schedule
import time
from user_config_control import UserConfig
from google_api.google_api_control import GoogleApiControl


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

        # schedule.every().day.at(user.get_notify_time()).do(api_control.check_assignments)
        # schedule.every().tuesday.at("22:44").do(api_control.notify_user)

    while True:
        print("Checking for scheduled run")
        schedule.run_pending()
        # Wait every 5 minutes before checking
        time.sleep(300)
