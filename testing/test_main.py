# from unittest.mock import patch, call
import unittest

# classes
from main import *

participants = [
    {
        "first": "John",
        "last": "Doe",
        "email": "fake1@gmail.com",
        "last_giftee": "Linda German",
    },
    {
        "first": "Brenda",
        "last": "Doe",
        "email": "fake2@gmail.com",
        "last_giftee": "Bill German",
    },
    {
        "first": "Linda",
        "last": "German",
        "email": "fake3@gmail.com",
        "last_giftee": "Brenda Doe",
    },
    {
        "first": "Bill",
        "last": "German",
        "email": "fake4@gmail.com",
        "last_giftee": "John Doe",
    },
]


class ValidPair(unittest.TestCase):
    """
    Tests `valid_pair` function.
    """

    def test_valid(self):
        person1 = {
            "first": "John",
            "last": "Doe",
            "email": "fake1@gmail.com",
            "last_giftee": "Linda German",
        }
        person2 = {
            "first": "Bill",
            "last": "German",
            "email": "fake4@gmail.com",
            "last_giftee": "John Doe",
        }
        self.assertTrue(valid_pair(person1, person2), "Should be True")

    def test_invalid(self):
        person1 = {
            "first": "John",
            "last": "Doe",
            "email": "fake1@gmail.com",
            "last_giftee": "Linda German",
        }
        person2 = {
            "first": "Linda",
            "last": "German",
            "email": "fake3@gmail.com",
            "last_giftee": "Brenda Doe",
        }
        self.assertFalse(valid_pair(person1, person2), "Should be False")


class ValidatePairs(unittest.TestCase):
    """
    Tests `validate_pairs` function.
    """

    def test_valid(self):
        pairs = [
            (
                {
                    "first": "John",
                    "last": "Doe",
                    "email": "fake1@gmail.com",
                    "last_giftee": "Linda German",
                },
                {
                    "first": "Bill",
                    "last": "German",
                    "email": "fake4@gmail.com",
                    "last_giftee": "John Doe",
                },
            ),
            (
                {
                    "first": "Brenda",
                    "last": "Doe",
                    "email": "fake2@gmail.com",
                    "last_giftee": "Bill German",
                },
                {
                    "first": "Linda",
                    "last": "German",
                    "email": "fake3@gmail.com",
                    "last_giftee": "Brenda Doe",
                },
            ),
        ]
        self.assertTrue(validate_pairs(pairs), "Should be True")

    def test_invalid(self):
        pairs = [
            (
                {
                    "first": "John",
                    "last": "Doe",
                    "email": "fake1@gmail.com",
                    "last_giftee": " Bill German",
                },
                {
                    "first": "Bill",
                    "last": "German",
                    "email": "fake4@gmail.com",
                    "last_giftee": "John Doe",
                },
            ),
            (
                {
                    "first": "Linda",
                    "last": "German",
                    "email": "fake3@gmail.com",
                    "last_giftee": "Brenda Doe",
                },
                {
                    "first": "Brenda",
                    "last": "Doe",
                    "email": "fake2@gmail.com",
                    "last_giftee": "Linda German",
                },
            ),
        ]
        self.assertFalse(validate_pairs(pairs), "Should be False")


if __name__ == "__main__":
    unittest.main()
