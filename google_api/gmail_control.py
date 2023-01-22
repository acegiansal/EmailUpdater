from user_config_control import UserConfig
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

m_logger = logging.getLogger(__name__)
m_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

m_file_handler = logging.FileHandler('logs/google_api.log')
m_file_handler.setFormatter(formatter)

m_logger.addHandler(m_file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

m_logger.addHandler(stream_handler)


class GmailControl:

    PORT = 465

    def __init__(self, user: UserConfig):
        self.user = user

    def send_email(self, message_info: dict):
        # Create a secure SSL context
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", self.PORT, context=context) as server:
                password = self.user.get_password()
                sender = self.user.get_sender()
                m_logger.info(f"Sending email to {sender}")
                server.login(sender, password)

                message = MIMEMultipart("alternative")
                message['Subject'] = message_info['Subject']
                message['From'] = self.user.get_sender()
                message['To'] = self.user.get_receiver()
                message.attach(self._formulate_email_body(message_info))

                server.send_message(message)
        except AttributeError as e:
            m_logger.exception(e)

    @staticmethod
    def _formulate_email_body(message_info: dict) -> MIMEText:
        html_text = f"<html><body>"

        html_text += f"<h2>{message_info['title']}</h2><hr>"

        for line in message_info['lines']:
            html_text += f"<p>{line}</p>"

        for link_name in message_info['links']:
            html_text += f"<a href='{message_info['links'][link_name]}'>{link_name}<a>"

        html_text += "</body></html>"

        return MIMEText(html_text, "html")


if __name__ == "__main__":
    testUser = {
        "sender": "giandevmail@gmail.com",
        "receiver": "acegiansal@gmail.com",
        "notify_time": "12:00",
        "google_sheet_link": "1_gwrr3jNRTdwfkp1i2O-AIvkxAhaERtXycZufN25Wso",
        "credentials_file_name": "credentials.json"
    }
    service_id = "EmailUpdater"

    testU = UserConfig(testUser, service_id)

    gmail_ct = GmailControl(testU)

    gmail_ct.send_email("Hello")
