from pathlib import Path
import datetime as dt
import random, json

from rich.console import Console
from rich.theme import Theme

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
    test_email = gmail["test_email"]

    Email = Email(gmail_username, gmail_password)

    # rich console
    custom_theme = Theme(
        {
            "prim": "bold deep_sky_blue1",
            "sec": "bold pale_turquoise1",
        }
    )
    console = Console(theme=custom_theme)

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

    def create_pairs(
        self, participants: list[dict], attempt_limit=1_000
    ) -> list[tuple]:
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

            attempt_limit -= 1
            if attempt_limit == 0:
                print("Failed to find a full set of valid pairs.")
                print("More or less particapants may be required.")
                exit()
        return pairs

    def create_email_body(self, gifter, giftee, perms):
        """
        ph
        """
        gifter_name = self.full_name(gifter)
        giftee_name = self.full_name(giftee)
        email_body = f"<h3>Hello {gifter_name},</h3>"
        email_body += f"\n\nYour Secret Santa match is:<br>\n{giftee_name}"

        # optional wishlist
        if "wishlist" in giftee.keys():
            wishlist = giftee["wishlist"]
            if wishlist:
                email_body += (
                    f"\n\n<br><br><a href='{wishlist}'>{giftee_name}'s Wishlist</a>\n"
                )

        # optional notes
        if "notes" in giftee.keys():
            notes = giftee["notes"]
            if notes:
                email_body += (
                    f"\n<br><br>Your giftee left the following notes:\n<br>{notes}"
                )

        # optional permutations info
        if perms:
            email_body += (
                f"\n\n<br><br>This was one of {perms:,} pairings for everyone."
            )

        email_body += f"\n\n<br><br>Merry Christmas!"

        return email_body

    def send_secret_santa_emails(self, pairs, perms=None):
        """
        ph
        """
        if self.debug:
            print("\nPairs:")
        for pair in pairs:
            gifter = pair[0]
            giftee = pair[1]
            gifter_name = self.full_name(gifter)
            giftee_name = self.full_name(giftee)

            if self.debug:
                self.console.print(f"\n[sec]{gifter_name}[/] to [sec]{giftee_name}[/]")
                self.console.print(f"Last Giftee: [sec]{gifter['last_giftee']}[/]")

            # email setup creation
            email_body = self.create_email_body(gifter, giftee, perms)

            # email body debug output
            email_body_test = ""
            if self.debug:
                if "Michael" in giftee_name:
                    email_body_test = email_body
                    self.Email.send_email(
                        subject=email_subject,
                        body=email_body,
                        to_email=recipient_email,
                        text="html",
                    )

            # recipient_email = gifter["email"]
            recipient_email = self.test_email

            email_subject = "Secret Santa Match"

            # non debug only email sending
            if not self.debug:
                self.console.print(f"Sending Email to [sec]{gifter_name}[/]")
                self.Email.send_email(
                    subject=email_subject,
                    body=email_body,
                    to_email=recipient_email,
                    text="html",
                )
        if self.debug and email_body_test:
            print("\nStart of Email")
            print("---------------")
            print(email_body_test)
            print("---------------")
            print("End of Email")

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
                    valid_pairs += 1
            combos.append(valid_pairs)
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
        self.console.print(
            f"[prim]Secret Santa Pair Picker[/] | [sec]{dt.datetime.now().year}[/]\n"
        )

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
        input()


if __name__ == "__main__":
    PairPicker = SecretSanta(debug=True)
    PairPicker.run()
