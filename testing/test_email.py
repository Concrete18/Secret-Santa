import unittest

# classes
from classes.email import Email


class ValidateEmail(unittest.TestCase):
    """
    Tests `validate_email` function.
    """

    def setUp(self):
        self.email = Email("gmail_username", "gmail_password")

    def test_valid_email(self):
        email = "michaeltest@gmail.com"
        valid = self.email.validate_email(email)
        self.assertTrue(valid, f"{email} should be considered a valid email")

    def test_invalid_email(self):
        email = "bad_email%test.yom"
        valid = self.email.validate_email(email)
        self.assertFalse(valid, f"{email} should be considered an invalid email")


if __name__ == "__main__":
    unittest.main()
