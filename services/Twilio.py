import os
from dataclasses import dataclass

from twilio.rest import Client


@dataclass
class Twilio:
    client: Client

    def __init__(self) -> None:
        self.client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

    def sendSMS(self, body) -> None:
        self.client.messages.create(
            body=body,
            from_=os.environ["TWILIO_VIRTUAL_PHONE_NO"],
            to=os.environ["MY_PHONE_NO"],
        )
