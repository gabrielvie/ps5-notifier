import os
import time
import dotenv
import colored
import requests
from datetime import datetime


class Notifier:
    url: str = "https://maker.ifttt.com/trigger/{event_name}/with/key/{ifttt_token}"

    event_name: str
    ifttt_token: str

    message_values: dict

    def __init__(self):
        """Initializes Notifier class."""
        dotenv.load_dotenv()
        self.event_name = os.getenv('IFTTT_EVENT_NAME')
        self.ifttt_token = os.getenv('IFTTT_TOKEN')

    def set_message_values(self, product: str, link: str):
        """Sets message values for IFTTT.

        Args:
            product (str): Product title.
            link (str): Product link.
        """
        self.message_values = {
            'value1': product,
            'value3': link,
        }

    def notify(self):
        """Send a notification to IFTTT webhook."""
        ifttt_webhook_url = self.url.format(
            event_name=self.event_name, ifttt_token=self.ifttt_token)
        requests.post(ifttt_webhook_url, json=self.message_values)

        print("%sNotification sent!%s" %
              (colored.fg(105), colored.attr(0)))
