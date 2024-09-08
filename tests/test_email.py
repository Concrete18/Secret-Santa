# local imports
from utils.email import Email


class TestValidateEmail:
    """
    Tests `validate_email` function.
    """

    email = Email("gmail_username", "gmail_password")

    def test_valid_email(self):
        email = "michaeltest3423@gmail.com"
        valid = self.email.validate_email(email)
        assert valid

    def test_invalid_email(self):
        email = "bad_email%test.yom"
        valid = self.email.validate_email(email)
        assert not valid
