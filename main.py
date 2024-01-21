from pathlib import Path
import datetime as dt
import random, json

from rich.console import Console
from rich.theme import Theme

from classes.email import Email


class SecretSanta:
    # get config data
    config = Path("config.json")
    with open(config) as file:
        data = json.load(file)
        gmail = data["gmail"]
        participants = data["participants"]

    # Gmail account details
    gmail_username = gmail["username"]
    gmail_password = gmail["password"]

    # settings
    # TODO make debug optional
    debug = data["settings"]["debug"]

    Email = Email(gmail_username, gmail_password)

    # rich console
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

    def create_email_body(self, gifter, giftee):
        """
        ph
        """
        gifter_name = self.full_name(gifter)
        giftee_name = self.full_name(giftee)
        head = """
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                }
                .container {
                    width: 100%;
                    margin: 0 auto;
                    padding: 10px;
                    background-color: #fff;
                    text-align: left;
                }
                h1 {
                    color: #e42626;
                    text-align: center;
                }
                h2 {
                    text-align: center;
                }
                h3 {
                    text-align: center;
                }
                p {
                    font-size: 16px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                    text-align: center;
                }
                a {
                    font-size: 16px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                    text-align: center;
                }

                .footer {
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        """

        contents = f"<h3>Hello {gifter_name},</h3>"
        contents += f"<p>Exciting news! You are the Secret Santa for:</p>"
        contents += f"<h2>{giftee_name}</h2><br>"

        # optional notes
        if "notes" in giftee.keys():
            notes = giftee["notes"]
            if notes:
                contents += f"<p>Your giftee left the following notes:</p>"
                contents += f"<p><em>{notes}</em></p><br>"

        # optional wishlist
        if "wishlist" in giftee.keys():
            wishlist = giftee["wishlist"]
            if wishlist:
                contents += f"<p>{giftee_name} Wishlist: <a href='{wishlist}'>Click Here</a></p>"

        body = f"""
        <body>
            <div class="container" align="center" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto;">
                <h1>Secret Santa Match Revealed!</h1>
                {contents}
                <p>Gift Price should be limited to $100 or less.</p>
                <p>Get ready to spread some holiday cheer and find the perfect gift for your Secret Santa match. Remember, it's all about the joy of giving!</p>
                <p>Wishing you a wonderful holiday season!</p>
                <div class="footer">
                    <p>Best Regards,</p>
                    <p>Your Secret Santa Organizer</p>
                </div>
            </div>
        </body>
        </html>
        """

        return head + body

    def send_secret_santa_emails(self, pairs):
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

            # email setup creation
            email_subject = "Secret Santa Match"
            recipient_email = gifter["email"]
            email_body = self.create_email_body(gifter, giftee)

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
            if (
                participant["last_giftee"]
                and participant["last_giftee"] not in full_names
            ):
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

        self.send_secret_santa_emails(pairs)
        input()


if __name__ == "__main__":
    PairPicker = SecretSanta()
    PairPicker.run()
