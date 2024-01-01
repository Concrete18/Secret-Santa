from pathlib import Path
import datetime as dt
import random, json

from classes.email import Email


class SecretSanta(Email):
    # get config data
    config = Path("config.json")
    with open(config) as file:
        data = json.load(file)
        gmail = data["gmail"]
        participants = data["participants"]

    # Gmail account details
    gmail_username = gmail["username"]
    gmail_password = gmail["password"]

    Email = Email(gmail_username, gmail_password)

    def __init__(self, debug=False) -> None:
        """
        ph
        """
        self.debug = debug

    @staticmethod
    def full_name(contact: dict) -> str:
        """
        Gets fullname for `contact`.
        """
        return f"{contact['first']} {contact['last']}"

    def valid_pair(self, person1: dict, person2: dict) -> bool:
        """
        Determines if `person1` and `person2` are a valid pair.
        """
        # same last name
        if person1["last"] == person2["last"]:
            return False
        # previous giftee
        if (
            person2["first"] in person1["last_giftee"]
            and person2["last"] in person1["last_giftee"]
        ):
            return False
        # same person
        if person1 == person2:
            return False
        return True

    def validate_pairs(self, pairs: list[dict]) -> bool:
        """
        Determines if the list of `pairs` are all valid.
        """
        unique_giftee = []
        for pair in pairs:
            gifter, giftee = pair[0], pair[1]
            if not self.valid_pair(gifter, giftee):
                return False
            giftee_full_name = self.full_name(giftee)
            if giftee_full_name in unique_giftee:
                return False
            unique_giftee.append(giftee_full_name)
        return True

    def create_pair(self, gifter: dict, possible_giftees: list[dict]) -> tuple[dict]:
        """
        Creates a single Secret Santa Pair based on rules determined by `valid_pair`.
        """
        for giftee in possible_giftees:
            if not self.valid_pair(giftee, gifter):
                continue
            possible_giftees.remove(giftee)
            pair = (gifter, giftee)
            return pair
        return {}

    def create_pairs(self, participants: list[dict]) -> list[tuple]:
        """
        ph
        """
        while True:
            possible_giftees = participants.copy()
            random.shuffle(possible_giftees)

            pairs = []
            for gifter in participants:
                new_pair = self.create_pair(gifter, possible_giftees)
                if new_pair:
                    pairs.append(new_pair)

            if self.validate_pairs(pairs) and len(pairs) == len(participants):
                break

        return pairs

    def send_secret_santa_emails(self, pairs, permutations="Unknown"):
        """
        ph
        """
        print("\nPairs:")
        for pair in pairs:
            gifter = pair[0]
            giftee = pair[1]

            gifter_name = self.full_name(gifter)
            giftee_name = self.full_name(giftee)
            if self.debug:
                print(f"{gifter_name} - {giftee_name} != {gifter['last_giftee']}")
                continue

            print(f"sending Email to {gifter_name}")

            recipient_email = gifter["email"]
            email_subject = "Secret Santa Match"
            email_body = f"Hello {gifter_name},\n\nYour Secret Santa match is: {giftee_name}.\n\nThis was one of {permutations:,} possiple pairings for everyone."
            self.Email.send_email(email_subject, email_body, recipient_email)
        print("\nProcess Complete")

    def get_permutations(self, participants):
        """
        ph
        """
        combos = []
        for gifter in participants:
            valid_pairs = 0
            for giftee in participants:
                if self.valid_pair(giftee, gifter):
                    print(giftee, gifter)
                    valid_pairs += 1
            combos.append(valid_pairs)
        print(combos)
        # find permutations
        permutations = 1
        for n in combos:
            permutations = permutations * n
        return permutations

    def validate_last_giftees(self, participants):
        """
        ph
        """
        full_names = [self.full_name(contact) for contact in participants]
        for participant in participants:
            if participant["last_giftee"] not in full_names:
                msg = f"Failed match {participant['last_giftee']} with anyone in participants list."
                input(msg)
                exit()

    def run(self):
        """
        ph
        """
        print(f"Secret Santa Pair Picker | {dt.datetime.now().year}\n")

        self.validate_last_giftees(self.participants)

        permutations = self.get_permutations(self.participants)
        print(f"There are {permutations:,} pair permutations.")

        pairs = self.create_pairs(self.participants)

        if not self.debug:
            msg = "\nDo you want to notify everyone who their secret santa is?\n"
            response = input(msg)
            if not response.lower() in ["yes", "y"]:
                input("\nCanceled")
                exit()

        self.send_secret_santa_emails(pairs, permutations)


if __name__ == "__main__":
    PairPicker = SecretSanta(debug=True)
    PairPicker.run()
