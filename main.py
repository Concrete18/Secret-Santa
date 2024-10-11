# standard library
from pathlib import Path
import datetime as dt
import random, json

# third-party imports
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

# local imports
from utils.email import Email
from utils.action_picker import action_picker


class Person:
    def __init__(self, data: dict) -> None:
        self.first_name = data.get("first", None)
        self.last_name = data.get("last", None)
        self.email = data.get("email", None)
        self.prev_giftee = data.get("prev_giftee", None)
        self.wishlist = data.get("wishlist", None)
        self.notes = data.get("wishlist", None)

    def __repr__(self) -> str:
        return (
            f"Person(\nfirst_name={self.first_name}, last_name={self.last_name}, "
            f"email={self.email}, prev_giftee={self.prev_giftee}, "
            f"wishlist={self.wishlist}, notes={self.notes})"
        )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class SecretSanta:
    config = Path("config.json")
    with open(config) as file:
        data = json.load(file)
        gmail = data.get("gmail", False)

        entries = []
        for person in data.get("entries", []):
            entries.append(Person(person))

        test_entries = []
        for test_person in data.get("test_entries", []):
            test_entries.append(Person(test_person))

    # Gmail account details
    gmail_username = gmail.get("username", False)
    gmail_password = gmail.get("password", False)
    test_email = gmail.get("test_email", False)
    email = Email(gmail_username, gmail_password)

    # rich console setup
    custom_theme = Theme(
        {
            "prim": "bold deep_sky_blue1",
            "sec": "bold pale_turquoise1",
            # christmas colors
            "theme-red": "bright_red",
            "theme-green": "bright_green",
        }
    )
    console = Console(theme=custom_theme)

    def is_valid_pair(
        self,
        gifter: Person,
        giftee: Person,
    ) -> bool:
        """
        Determines if `gifter` and `giftee` are a valid pair.
        """
        # same last name
        if gifter.last_name == giftee.last_name:
            return False
        # previous giftee
        if gifter.prev_giftee == giftee.full_name:
            return False
        # same person
        if gifter == giftee:
            return False
        return True

    def validate_pairs(self, pairs: list[list[Person, Person]]) -> bool:
        """
        Determines if the list of `pairs` are all valid.
        """
        unique_giftee = []
        for pair in pairs:
            gifter, giftee = pair[0], pair[1]
            if not self.is_valid_pair(gifter, giftee):
                return False
            if giftee.full_name in unique_giftee:
                return False
            unique_giftee.append(giftee.full_name)
        return True

    def find_valid_pair(
        self,
        gifter: Person,
        possible_giftees: list[Person],
    ) -> tuple[Person, Person]:
        """
        Finds a single Secret Santa Pair based on rules determined by `valid_pair` and returns it.
        """
        for giftee in possible_giftees:
            if not self.is_valid_pair(gifter, giftee):
                continue
            possible_giftees.remove(giftee)
            return (gifter, giftee)
        return {}

    def create_pairs(
        self,
        entries: list[Person],
        attempt_limit=1_000,
    ) -> list[tuple[Person, Person]]:
        """
        Creates pairs from `entries` and checks if they are valid until the a
        valid pair is found or the `attempt_limit` is reached.
        """
        while True:
            possible_giftees = entries.copy()
            random.shuffle(possible_giftees)

            pairs = []
            for gifter in entries:
                new_pair = self.find_valid_pair(gifter, possible_giftees)
                if new_pair:
                    pairs.append(new_pair)

            if self.validate_pairs(pairs) and len(pairs) == len(entries):
                break

            attempt_limit -= 1
            if attempt_limit == 0:
                print("Failed to find a full set of valid pairs.")
                print("More or less particapants may be required.")
                exit()
        return pairs

    def create_html(self, data: str, write_to_file: bool = False) -> None:
        """
        Creates an html file with the given `data`.
        Writes to a file if `write_to_file` is True.
        """
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("christmas_card_template.html")
        html_content = template.render(data)
        # writes to a file for local testing
        if write_to_file:
            with open("test.html", "w") as file:
                file.write(html_content)
        return html_content

    def create_test_email(self) -> None:
        """
        Creates a HTML test file.
        """
        self.create_html(
            data={
                "gifter_name": "John Smith",
                "giftee_name": "Jane Doe",
                "wishlist": "https://www.giftster.com/list/A5IgT/",
                "notes": "Test Notes Here.",
            },
            write_to_file=True,
        )
        # TODO Ask to open in browser

    def show_entries_table(self, entries: list[Person]) -> None:
        """
        Shows Entry Data with a table.
        """
        table = Table(
            title="Secret Santa Entries",
            show_lines=True,
            title_style="bold",
            style="theme-green",
        )
        table.add_column("First Name", justify="left")
        table.add_column("Last Name", justify="left")
        table.add_column("Email", justify="left")
        table.add_column("Last Giftee", justify="left")
        table.add_column("Wishlist Link", justify="left")

        for entry in entries:
            row = [
                entry.first_name,
                entry.last_name,
                entry.email,
                entry.prev_giftee,
                entry.wishlist,
            ]
            table.add_row(*row)

        self.console.print(table, new_line_start=True)

    def send_secret_santa_emails(
        self,
        pairs: list[list[Person, Person]],
        test: bool = False,
    ) -> None:
        """
        Sends emails to all entries for Secret Santa.
        """
        print("\nPairs:")

        for gifter, giftee in pairs:

            self.console.print(f"\nSending email to [sec]{gifter.full_name}[/]")

            if test:
                self.console.print(f"New Giftee [sec]{giftee.full_name}[/]")

                last_giftee = gifter.prev_giftee if gifter.prev_giftee else "Unset"
                self.console.print(f"Last Giftee: [sec]{last_giftee}[/]")

            # email
            email_subject = "Secret Santa Match"
            email_body = self.create_html(
                {
                    "gifter_name": gifter.full_name,
                    "giftee_name": giftee.full_name,
                    "notes": giftee.notes,
                    "wishlist_link": giftee.wishlist,
                }
            )

            try:
                self.email.send_email(
                    subject=email_subject,
                    body=email_body,
                    to_email=gifter.email,
                    text="html",
                )
            except Exception as e:
                msg = f"Failed to send email to [sec]{gifter.full_name}[/]: {e}"
                self.console.print(msg)

        print("\nProcess Complete")

    def get_permutations_count(self, entries: list[Person]) -> int:
        """
        Gets the total permutations count for `entries`.
        """
        combos = []
        for gifter in entries:
            valid_pairs = 0
            for giftee in entries:
                if self.is_valid_pair(giftee, gifter):
                    valid_pairs += 1
            combos.append(valid_pairs)
        # find permutations
        permutations = 1
        for n in combos:
            permutations = permutations * n
        return permutations

    def validate_emails(self, entries: list[Person]) -> None:
        """
        Validates emails for `entries`.
        """
        for entry in entries:
            if not self.email.validate_email(entry.email):
                msg = f"{entry.email} for {entry.full_name} is not a valid email."
                input(msg)
                exit()

    def validate_prev_giftees(self, entries: list[Person]) -> None:
        """
        Validates each entries last giftee to be sure they are found within `entries`.
        """
        full_names = [entry.full_name for entry in entries]
        for entry in entries:
            if entry.prev_giftee and entry.prev_giftee not in full_names:
                msg = f"Failed to match {entry.prev_giftee} with anyone."
                input(msg)
                exit()

    def create_test_pairs(self) -> None:
        """
        Creates pairs only for testing to confirm pairs are valid.
        """
        table = Table(
            title="Test Pairs",
            show_lines=True,
            title_style="bold",
            style="theme-green",
        )
        table.add_column("Gifter Name", justify="left")
        table.add_column("Gifter's\nLast Giftee", justify="left")
        table.add_column("Giftee Name", justify="left")
        table.add_column("Same\nLast Name", justify="center")

        pairs = self.create_pairs(self.entries)
        for pair in pairs:
            gifter, giftee = pair
            row = [
                gifter.full_name,
                gifter.prev_giftee,
                giftee.full_name,
                str(gifter.last_name == giftee.last_name),
            ]
            table.add_row(*row)

        self.console.print(table, new_line_start=True)

    def create_pairs_and_send(self, entries: list[Person], test=False) -> None:
        """
        Creates pairs from `entires` and sends the emails out.
        """
        if test:
            print("\nStarting Test")

        self.validate_emails(entries)
        self.validate_prev_giftees(entries)

        permutations = self.get_permutations_count(entries)
        print(f"\nThere are {permutations:,} pair permutations.")

        print("\nEmails will be sent to the following addresses:")
        for entry in entries:
            print(entry.email)

        msg = "\nDo you want to notify everyone who their Secret Santa is?\n"
        response = input(msg)
        if not response.lower() in ["yes", "y"]:
            input("\nCancelled")
            return

        pairs = self.create_pairs(entries)
        self.send_secret_santa_emails(pairs=pairs, test=test)
        input()

    def menu_actions(self) -> None:
        main_run = lambda: self.create_pairs_and_send(self.entries)
        test_run = lambda: self.create_pairs_and_send(self.test_entries, test=True)
        choices = [
            ("Send Secret Santa Emails", main_run),
            ("Send Test Emails", test_run),
            ("Create Test Pairs", self.create_test_pairs),
            ("Create Test HTML File", self.create_test_email),
            ("Show Entries Table", lambda: self.show_entries_table(self.entries)),
            ("Exit", exit),
        ]
        action_picker(choices)
        exit()

    def main(self) -> None:
        year = dt.datetime.now().year
        title = f"[theme-green]Secret Santa Pair Picker[/] | [theme-red]{year}[/]"
        self.console.print(title)

        self.show_entries_table(self.entries)

        self.menu_actions()


if __name__ == "__main__":
    App = SecretSanta()
    App.main()
