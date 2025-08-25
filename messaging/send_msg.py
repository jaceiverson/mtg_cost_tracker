import json
import os

import requests
from dotenv import load_dotenv
from rich import print
from twilio.rest import Client

load_dotenv()


def send_text(message: str) -> bool:
    # Create Twilio client
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN"),
    )

    # Send SMS
    # in body part you have to write your message
    sent_message = client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=os.getenv("RECIPIENT_PHONE_NUMBER"),
    )

    print(f"[green]Message sent with SID: {sent_message.sid}[/green]")

    return True


def send_whats_app(message: str) -> bool:
    url = "https://messages-sandbox.nexmo.com/v1/messages"

    payload = json.dumps(
        {
            "from": os.environ["WHATS_APP_PHONE_NUMBER"],
            "to": os.environ["RECIPIENT_PHONE_NUMBER"],
            "message_type": "text",
            "text": message,
            "channel": "whatsapp",
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": os.environ["WHATS_APP_AUTH_TOKEN_FROM_POSTMAN"],
    }

    response = requests.post(url, headers=headers, data=payload)

    print(f"[blue]Message sent: {response.json()['message_uuid']}[/blue]")
    return True
