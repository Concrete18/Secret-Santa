# standard library
import random, string

# local imports
from main import SecretSanta, Person


class TestIsValidPair:
    """
    Tests `is_valid_pair` function.
    """

    ss = SecretSanta()

    def test_valid(self):
        person1 = Person(
            {
                "first": "John",
                "last": "Doe",
                "email": "fake1@gmail.com",
                "prev_giftee": "Linda German",
            }
        )
        person2 = Person(
            {
                "first": "Bill",
                "last": "German",
                "email": "fake4@gmail.com",
                "prev_giftee": "John Doe",
            }
        )
        assert self.ss.is_valid_pair(person1, person2)

    def test_invalid(self):
        person1 = Person(
            {
                "first": "John",
                "last": "Doe",
                "email": "fake1@gmail.com",
                "prev_giftee": "Linda German",
            }
        )
        person2 = Person(
            {
                "first": "Linda",
                "last": "German",
                "email": "fake3@gmail.com",
                "prev_giftee": "Brenda Doe",
            }
        )
        assert not self.ss.is_valid_pair(person1, person2)

    def test_same_person(self):
        person1 = Person(
            {
                "first": "John",
                "last": "Doe",
                "email": "fake1@gmail.com",
                "prev_giftee": "Linda German",
            }
        )
        assert not self.ss.is_valid_pair(person1, person1)


class TestFindValidPair:
    """
    Tests `is_valid_pair` function.
    """

    ss = SecretSanta()

    def test_valid(self):
        gifter = Person(
            {
                "first": "Bill",
                "last": "German",
                "prev_giftee": "John Doe",
            }
        )
        data = [
            {
                "first": "John",
                "last": "Doe",
                "prev_giftee": "Linda German",
            },
            {
                "first": "Jane",
                "last": "Doe",
                "prev_giftee": "Bill German",
            },
            {
                "first": "Linda",
                "last": "German",
                "prev_giftee": "Jane Doe",
            },
            {
                "first": "Ryan",
                "last": "Bickman",
                "prev_giftee": "",
            },
            {
                "first": "Ellie",
                "last": "Bickman",
                "prev_giftee": "",
            },
        ]
        entries = [Person(entry) for entry in data]
        random.shuffle(entries)
        gifter, giftee = self.ss.find_valid_pair(gifter, entries)
        assert giftee.last_name != "German"
        assert gifter.prev_giftee != giftee.full_name
        assert gifter.last_name != giftee.last_name


class TestValidatePairs:
    """
    Tests `validate_pairs` function.
    """

    ss = SecretSanta()

    def test_valid(self):
        pairs = [
            (
                Person(
                    {
                        "first": "John",
                        "last": "Doe",
                        "email": "fake1@gmail.com",
                        "prev_giftee": "Linda German",
                    }
                ),
                Person(
                    {
                        "first": "Bill",
                        "last": "German",
                        "email": "fake4@gmail.com",
                        "prev_giftee": "John Doe",
                    },
                ),
            ),
            (
                Person(
                    {
                        "first": "Brenda",
                        "last": "Doe",
                        "email": "fake2@gmail.com",
                        "prev_giftee": "Bill German",
                    }
                ),
                Person(
                    {
                        "first": "Linda",
                        "last": "German",
                        "email": "fake3@gmail.com",
                        "prev_giftee": "Brenda Doe",
                    }
                ),
            ),
        ]
        assert self.ss.validate_pairs(pairs)

    def test_invalid(self):
        pairs = [
            (
                Person(
                    {
                        "first": "John",
                        "last": "Doe",
                        "email": "fake1@gmail.com",
                        "prev_giftee": " Bill German",
                    }
                ),
                Person(
                    {
                        "first": "Bill",
                        "last": "German",
                        "email": "fake4@gmail.com",
                        "prev_giftee": "John Doe",
                    }
                ),
            ),
            (
                Person(
                    {
                        "first": "Linda",
                        "last": "German",
                        "email": "fake3@gmail.com",
                        "prev_giftee": "Brenda Doe",
                    }
                ),
                Person(
                    {
                        "first": "Brenda",
                        "last": "Doe",
                        "email": "fake2@gmail.com",
                        "prev_giftee": "Linda German",
                    },
                ),
            ),
        ]
        assert not self.ss.validate_pairs(pairs)


class TestGetPermutationsCount:
    """
    Tests `get_permutations_count` function.
    """

    ss = SecretSanta()

    def test_permutations(self):
        data = [
            {
                "first": "John",
                "last": "Doe",
                "prev_giftee": "Linda German",
            },
            {
                "first": "Jane",
                "last": "Doe",
                "prev_giftee": "Bill German",
            },
            {
                "first": "Linda",
                "last": "German",
                "prev_giftee": "Jane Doe",
            },
            {
                "first": "Bill",
                "last": "German",
                "prev_giftee": "John Doe",
            },
            {
                "first": "Ryan",
                "last": "Bickman",
                "prev_giftee": "",
            },
            {
                "first": "Ellie",
                "last": "Bickman",
                "prev_giftee": "",
            },
        ]
        entries = [Person(entry) for entry in data]
        permutations = self.ss.get_permutations_count(entries)
        assert permutations == 1296


class TestCreatePairs:
    """
    Tests `create_pairs` function.
    """

    ss = SecretSanta()

    @staticmethod
    def generate_random_string(length: int) -> str:
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    def generate_random_entries(self, length: int) -> list[Person]:
        entries = []
        for _ in range(length):
            first_name = self.generate_random_string(5)
            last_name = self.generate_random_string(5)
            entry = {"first": first_name, "last": last_name}
            entries.append(Person(entry))
        original_entry_order = random.sample(entries, len(entries))
        random.shuffle(entries)
        for entry in original_entry_order:
            entry.prev_giftee = entry.full_name
        return entries

    def test_create_pairs(self):
        entries = self.generate_random_entries(4)
        pairs = self.ss.create_pairs(entries)
        print(pairs)
