import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, gmail_username, gmail_password) -> None:
        """
        ph
        """
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password

    def send_email(self, subject, body, to_email):
        """
        Sends an email with `subject` and `body` to the `to_email`.
        """
        message = MIMEMultipart()
        message["From"] = self.gmail_username
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        # message.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.gmail_username, self.gmail_password)
            server.sendmail(self.gmail_username, to_email, message.as_string())
