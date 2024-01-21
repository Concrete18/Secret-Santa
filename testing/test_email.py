import unittest

# classes
from classes.email import Email


class FullName(unittest.TestCase):
    """
    Tests `full_name` function.
    """

    def setUp(self):
        self.email = Email("gmail_username", "gmail_password")

    def test_generate_html(self):
        title = "This is the title"
        message = "Message is here."
        styles = {
            "div": "color: #fff; padding: 20px;",
            "h1": "background-color: #e44d26;",
        }
        output = self.email.generate_html(title, message, styles)
        answer = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>This is the title</title>
                    <style>
                        /* Add your default styles here */
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            margin: 0;
                            padding: 0;
                            text-align: center;
                        }
                        /* Add any additional styles provided as arguments */
                        div { color: #fff; padding: 20px; }h1 { background-color: #e44d26; }
                    </style>
                </head>
                <body>
                    <div>
                        <h1>This is the title</h1>
                        <p>Message is here.</p>
                    </div>
                </body>
            </html>
        """
        self.assertEqual(output, answer, "ph")


if __name__ == "__main__":
    unittest.main()
