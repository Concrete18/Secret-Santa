# Secret Santa

## Purpose

This was made for family Secret Santa. I thought it would be fun to make my own that is more likely to follow rules for picking pairs that we wanted.

## Features

- Creates pairs matching last names and last giftee disallowed
- Sends emails to all contacts with their pair
- Provides a link to the giftee's wishlist and additional notes if either are provided in the config

## Documentation

Use of Secret Santa should be rather easy for anyone familiar with Python and JSON.

### Dependencies

Run the following command to install dependencies.

```
pip install -r requirements.txt
```

### Config

Create a config file named config.json and fill it as the example below is shown. Make sure to include many participants as the example just includes one.

#### Config Example

```json
{
  "gmail": {
    "test_email": "Insert Test Email",
    "username": "Insert Gmail set up for sending",
    "password": "Insert Gmail App Password"
  },
  "participants": [
    {
      "first": "John",
      "last": "Smith",
      "email": "test@gmail.com",
      "last_giftee": "Jane Doe",
      "notes": "Optional - Insert Notes",
      "wishlist": "Optional - Insert wishlist link"
    }
  ]
}
```

### Run

Once you have all the dependencies and have set up the config, just run the python script and it will find valid pairs and send them emails with their pairs for you. As long as you do not look at the sent emails with the gmail account or turn on the debug settings, you will not know who has who.
