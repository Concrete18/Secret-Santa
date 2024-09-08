import smtplib, ssl, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, gmail_username: str, gmail_password: str) -> None:
        """
        Python Email functionality.
        """
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Verifies if an email is valid using regex.
        """
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        return re.fullmatch(regex, email)

    def send_email(
        self,
        subject: str,
        body: str,
        to_email: str,
        text: str = "plain",
    ) -> None:
        """
        Sends an email with `subject` and `body` to the `to_email`.
        Body can be set to plain text or html by setting the `text` arg.
        """
        message = MIMEMultipart()
        message["From"] = self.gmail_username
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, text))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.gmail_username, self.gmail_password)
            server.sendmail(self.gmail_username, to_email, message.as_string())
