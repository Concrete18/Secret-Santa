from pathlib import Path
import random, json

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def full_name(pair):
    """
    ph
    """
    return f"{pair['first']} {pair['last']}"


def valid_pair(person1, person2):
    """
    ph
    """
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
    """
    ph
    """
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
    """
    ph
    """
    for giftee in possible_giftees:
        if not valid_pair(giftee, gifter):
            continue
        possible_giftees.remove(giftee)
        pair = (gifter, giftee)
        return pair
    return False


def create_pairs(participants: list[dict]) -> list[tuple]:
    """
    ph
    """
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


def send_email(config, subject, body, to_email):
    """
    ph
    """
    # Gmail account details
    gmail_user = config["gmail_username"]
    gmail_password = config["gmail_password"]

    # Create the MIMEText and MIMEMultipart objects
    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, message.as_string())


def send_secret_santa_emails(config, pairs, permutations="Unknown"):
    """
    ph
    """
    print("\nPairs:")
    for pair in pairs:
        gifter = pair[0]
        giftee = pair[1]

        # debug
        gifter_name = f"{gifter['first']} {gifter['last']}"
        giftee_name = f"{giftee['first']} {giftee['last']}"
        print(f"{gifter_name} - {giftee_name}")

        recipient_email = gifter["email"]
        email_subject = "Secret Santa Match"
        email_body = f"Hello {full_name(gifter)},\n\nYour Secret Santa match is: {full_name(giftee)}.\n\nThis was one of {permutations:,} possiple pairings for everyone."
        send_email(config, email_subject, email_body, recipient_email)


def get_permutations(participants):
    """
    ph
    """
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
    return permutations


def validate_last_giftees(participants):
    """
    ph
    """
    full_names = [full_name(contact) for contact in participants]
    for participant in [full_name(contact) for contact in participants]:
        if participant["last_giftee"] not in full_names:
            msg = f"Failed match {participant['last_giftee']} with anyone in participants list."
            input(msg)
            exit()


def main():
    # get config data
    config = Path("config.json")
    with open(config) as file:
        data = json.load(file)
        config = data["config"]
        participants = data["contacts"]

    print("Secret Santa Pair Picker")

    validate_last_giftees(participants)

    permutations = get_permutations(participants)
    msg = f"There are {permutations:,} permutations"
    print(msg)

    pairs = create_pairs(participants)

    response = input("\nDo you want to notify everyone who their secret santa is?\n")
    if not response.lower() in ["yes", "y"]:
        input("\nCanceled")
        exit()

    send_secret_santa_emails(config, pairs, permutations)


if __name__ == "__main__":
    main()
