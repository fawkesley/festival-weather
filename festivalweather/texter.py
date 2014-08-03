from __future__ import unicode_literals

import os

from twilio.rest import TwilioRestClient


def send_sms(message):
    account = os.environ['TWILIO_SID']
    token = os.environ['TWILIO_AUTH_TOKEN']
    from_number = os.environ['TWILIO_FROM_NUMBER']
    recipients = os.environ['RECIPIENT_NUMBERS'].split(',')

    client = TwilioRestClient(account=account, token=token)

    for recipient in recipients:
        client.messages.create(
            from_=from_number,
            to=recipient,
            body=message
        )
