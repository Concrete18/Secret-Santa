from pathlib import Path
import random, json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def full_name(pair):
    return f"{pair['first']} {pair['last']}"


def valid_pair(person1, person2):
    # invalid pair
    if person1["last"] == person2["last"]:
        return False
    # previous giftee
    if person1["last_giftee"] == full_name(person2):
        return False
    # same person
    if person1 == person2:
        return False
    return True


def validate_pairs(pairs):
    unique_giftee = []
    for pair in pairs:
        gifter, giftee = pair[0], pair[1]
        if valid_pair(gifter, gifter):
            return False
        giftee_full_name = full_name(giftee)
        if giftee_full_name in unique_giftee:
            return False
        unique_giftee.append(giftee_full_name)
    return True


def create_pair(gifter, possible_giftees):
    for giftee in possible_giftees:
        if not valid_pair(giftee, gifter):
            continue
        possible_giftees.remove(giftee)
        pair = (gifter, giftee)
        return pair
    return False


def create_pairs(participants: list[dict]) -> list[tuple]:
    possible_giftees = participants.copy()
    random.shuffle(possible_giftees)

    pairs = []
    for gifter in participants:
        new_pair = create_pair(gifter, possible_giftees)
        if new_pair:
            pairs.append(new_pair)

    if not validate_pairs(pairs) or len(pairs) != len(participants):
        pairs = create_pairs(participants)

    return pairs


def send_secret_santa_emails(pairs):
    # Email configuration (replace with your SMTP server details)
    smtpserver = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "your_username"
    smtp_password = "your_password"
    sender_email = "your_email@example.com"

    # Loop through participants and send emails
    print("\nPairs:")
    for pair in pairs:
        recipient_email = pair[0]["email"]
        subject = "Secret Santa Match"

        gifter = pair[0]
        giftee = pair[1]
        print(
            f"{gifter['first']} {gifter['last']} - {giftee['first']} {giftee['last']}"
        )

        # recipient_email = participant["email"]
        # subject = "Secret Santa Match"
        # body = f"Hello {gifter},\n\nYour Secret Santa match is: {giftee}."

        # # Create MIMEText and MIMEMultipart objects for email content
        # msg = MIMEMultipart()
        # msg.attach(MIMEText(body, "plain"))
        # msg["Subject"] = subject
        # msg["From"] = sender_email
        # msg["To"] = recipient_email

        # # Connect to the SMTP server and send the email
        # with smtplib.SMTP(smtp_server, smtp_port) as server:
        #     server.starttls()
        #     server.login(smtp_username, smtp_password)
        #     server.sendmail(sender_email, recipient_email, msg.as_string())


def find_total_variations(participants):
    combos = []
    for gifter in participants:
        valid_pairs = 0
        for giftee in participants:
            if valid_pair(giftee, gifter):
                valid_pairs += 1
        combos.append(valid_pairs)
    # find permutations
    permutations = 1
    for n in combos:
        permutations = permutations * n
    msg = f"There are {permutations:,} permutations"
    print(msg)
    response = input("\nDo you want to notify everyone who their secret santa is?\n")
    if not response.lower() in ["yes", "y"]:
        input("\nCanceled")


def validate_last_giftees(participants):
    full_names = [full_name(contact) for contact in participants]
    for participant in participants:
        if participant["last_giftee"] not in full_names:
            msg = f"Failed match {participant['last_giftee']} with anyone in participants list."
            input(msg)


def main():
    config = Path("contacts.json")
    with open(config) as file:
        participants = json.load(file)

    print("Secret Santa Pair Picker")

    validate_last_giftees(participants)

    # find_total_variations(participants)

    for _ in range(15_000):
        pairs = create_pairs(participants)

    pairs = create_pairs(participants)

    send_secret_santa_emails(pairs)


if __name__ == "__main__":
    main()
