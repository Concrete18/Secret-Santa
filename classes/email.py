import smtplib, ssl
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
    def generate_html(
        title: str,
        message: str,
        styles: dict = None,
    ) -> str:
        """
        Creates a basic HTML string for sending as an email.

        Styles Example:
        >>> styles = {
        >>>    "div": "background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);",
        >>>    "h1": "color: #e44d26;",
        >>> }
        """
        styles = styles or {}
        styles_str = "".join(
            f"{selector} {{ {styles[selector]} }}" for selector in styles
        )
        # Construct the HTML content
        html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>{title}</title>
                    <style>
                        /* Add your default styles here */
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            margin: 0;
                            padding: 0;
                            text-align: center;
                        }}
                        /* Add any additional styles provided as arguments */
                        {styles_str}
                    </style>
                </head>
                <body>
                    <div>
                        <h1>{title}</h1>
                        <p>{message}</p>
                    </div>
                </body>
            </html>
        """
        return html_content

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
