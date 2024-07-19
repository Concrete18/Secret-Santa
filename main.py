# builtin
from pathlib import Path
import datetime as dt
import random, json

# installed
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.theme import Theme

# local
from classes.email import Email


class SecretSanta:
    # get config data
    config = Path("config.json")
    with open(config) as file:
        data = json.load(file)
        gmail = data.get("gmail", False)
        participants = data.get("participants", [])

    # Gmail account details
    gmail_username = gmail.get("username", False)
    gmail_password = gmail.get("password", False)
    test_email = gmail.get("test_email", False)

    # settings
    debug = data.get("settings", {}).get("debug", False)

    Email = Email(gmail_username, gmail_password)

    # rich console setup
    custom_theme = Theme(
        {
            "prim": "bold deep_sky_blue1",
            "sec": "bold pale_turquoise1",
        }
    )
    console = Console(theme=custom_theme)

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
        Creates pairs from `participants` and checks if they are valid until the a
        valid pair is found or the `attempt_limit` is reached.
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

    def create_html(self, data):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("christmas_card_template.html")
        html_content = template.render(data)
        # writes to a file for local testing
        if self.debug:
            with open("test.html", "w") as file:
                file.write(html_content)
        return html_content

    def send_secret_santa_emails(self, pairs):
        """
        Sends emails to all participants for Secret Santa.
        """
        if self.debug:
            print("\nPairs:")

        for pair in pairs:
            gifter, giftee = pair
            gifter_name = self.full_name(gifter)
            giftee_name = self.full_name(giftee)

            # email setup creation
            email_subject = "Secret Santa Match"
            recipient_email = gifter["email"]

            data = {
                "gifter_name": gifter_name,
                "giftee_name": giftee_name,
                "notes": giftee["notes"],
                "wishlist_link": giftee["wishlist"],
            }

            email_body = self.create_html(data)

            if self.debug:
                self.console.print(f"\n[sec]{gifter_name}[/] to [sec]{giftee_name}[/]")
                if not gifter["last_giftee"]:
                    gifter["last_giftee"] = "Unset"
                self.console.print(f"Last Giftee: [sec]{gifter['last_giftee']}[/]")
                if giftee_name == self.full_name(self.participants[0]):
                    self.Email.send_email(
                        subject=email_subject,
                        body=email_body,
                        to_email=recipient_email,
                        text="html",
                    )
            else:
                self.console.print(f"Sending Email to [sec]{gifter_name}[/]")
                self.Email.send_email(
                    subject=email_subject,
                    body=email_body,
                    to_email=recipient_email,
                    text="html",
                )

        print("\nProcess Complete")

    def get_permutations_count_count(self, participants):
        """
        Gets the total permutations count for `participants`.
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

    def validate_emails(self, participants):
        """
        Validates emails for `participants`.
        """
        for participant in participants:
            email = participant["email"]
            full_name = self.full_name(participant)
            if self.Email.validate_email(""):
                msg = f"{email} for {full_name} is not a valid email."
                input(msg)
                exit()

    def validate_last_giftees(self, participants):
        """
        Validates each participants last giftee to be sure they are found within `participants`.
        """
        full_names = [self.full_name(contact) for contact in participants]
        for participant in participants:
            last_giftee = participant["last_giftee"]
            if last_giftee and last_giftee not in full_names:
                msg = f"Failed to match {participant['last_giftee']} with anyone in participants list."
                input(msg)
                exit()

    def run(self):
        year = dt.datetime.now().year
        title = f"[prim]Secret Santa Pair Picker[/] | [sec]{year}[/]\n"
        self.console.print(title)

        # validationms
        self.validate_emails(self.participants)
        self.validate_last_giftees(self.participants)

        permutations = self.get_permutations_count(self.participants)
        print(f"There are {permutations:,} pair permutations.")

        pairs = self.create_pairs(self.participants)

        if not self.debug:
            print("\nEmails will be sent to the following addresses:")
            for participant in self.participants:
                print(participant["email"])

            msg = "\nDo you want to notify everyone who their Secret Santa is?\n"
            response = input(msg)
            if not response.lower() in ["yes", "y"]:
                input("\nCancelled")
                exit()
            print()

        self.send_secret_santa_emails(pairs)
        input()


if __name__ == "__main__":
    PairPicker = SecretSanta()
    # data = {
    #     "gifter_name": "Michael Ericson",
    #     "giftee_name": "Brian Napier",
    #     "wishlist_link": "https://www.giftster.com/list/A5IgT/",
    #     "notes": "Test Notes Here.",
    # }
    # PairPicker.create_html(data)
    # exit()
    PairPicker.run()
