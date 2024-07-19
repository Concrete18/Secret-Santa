import unittest
import random, string

# classes
from main import SecretSanta


class FullName(unittest.TestCase):
    """
    Tests `full_name` function.
    """

    def setUp(self):
        self.ss = SecretSanta()

    def test_full_name(self):
        contact = {
            "first": "John",
            "last": "Doe",
            "email": "fake1@gmail.com",
            "last_giftee": "Linda German",
        }
        self.assertEqual(self.ss.full_name(contact), "John Doe", "Should be John Doe")


class ValidPair(unittest.TestCase):
    """
    Tests `valid_pair` function.
    """

    def setUp(self):
        self.ss = SecretSanta()

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
        self.assertTrue(self.ss.valid_pair(person1, person2), "Should be True")

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
        self.assertFalse(self.ss.valid_pair(person1, person2), "Should be False")


class ValidatePairs(unittest.TestCase):
    """
    Tests `validate_pairs` function.
    """

    def setUp(self):
        self.ss = SecretSanta()

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
        self.assertTrue(self.ss.validate_pairs(pairs), "Should be True")

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
        self.assertFalse(self.ss.validate_pairs(pairs), "Should be False")


class GetPermutations(unittest.TestCase):
    """
    Tests `get_permutations_count` function.
    """

    def setUp(self):
        self.ss = SecretSanta()

    def test_permutations(self):
        participants = [
            {
                "first": "John",
                "last": "Doe",
                "last_giftee": "Linda German",
            },
            {
                "first": "Jane",
                "last": "Doe",
                "last_giftee": "Bill German",
            },
            {
                "first": "Linda",
                "last": "German",
                "last_giftee": "Jane Doe",
            },
            {
                "first": "Bill",
                "last": "German",
                "last_giftee": "John Doe",
            },
            {
                "first": "Ryan",
                "last": "Bickman",
                "last_giftee": "",
            },
            {
                "first": "Ellie",
                "last": "Bickman",
                "last_giftee": "",
            },
        ]
        permutations = self.ss.get_permutations_count(participants)
        self.assertEqual(permutations, 1296, "Should have 1296 permutations")


class CreatePairs(unittest.TestCase):
    """
    Tests `create_pairs` function.
    """

    def setUp(self):
        self.ss = SecretSanta()

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    def generate_random_participants(self, length):
        # {
        #     "first": "John",
        #     "last": "Doe",
        #     "last_giftee": "Linda German",
        # },
        participants = []
        for _ in range(length):
            first_name = self.generate_random_string(5)
            last_name = self.generate_random_string(5)
            entry = {"first": first_name, "last": last_name}
            participants.append(entry)
        original_participants_order = random.sample(participants, len(participants))
        random.shuffle(participants)
        for participant in original_participants_order:
            participant["last_giftee"] = self.ss.full_name(participant)
        return participants

    def test_create_pairs(self):
        participants = self.generate_random_participants(4)
        # print(participants)
        pairs = self.ss.create_pairs(participants)
        print(pairs)


if __name__ == "__main__":
    unittest.main()
