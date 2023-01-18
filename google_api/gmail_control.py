from user_config_control import UserConfig
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailControl:

    PORT = 465

    def __init__(self, user: UserConfig):
        self.user = user

    def send_email(self, message_info: dict):
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.PORT, context=context) as server:
            password = self.user.get_password()
            sender = self.user.get_sender()
            print(f"({sender}, {password})")
            server.login(sender, password)

            message = MIMEMultipart("alternative")
            message['Subject'] = 'Structured Test'
            message['From'] = self.user.get_sender()
            message['To'] = self.user.get_receiver()
            message.attach(self._formulate_email_body(message_info))

            server.send_message(message)

    @staticmethod
    def _formulate_email_body(message_info: dict) -> MIMEText:
        html_text = f"""\
        <html>
            <body>
                <h2><b>{message_info['title']}</b></h2>
                <hr>
                <p>{message_info['line1']}</p>
                <p>{message_info['line2']}</p>
                <p>{message_info['line3']}</p>
                <hr>
                <a href='https://brightspace.carleton.ca/d2l/home'>Link to Brightspace<a>
            </body>
        </html
        """
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
