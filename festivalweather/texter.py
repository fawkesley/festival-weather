from __future__ import unicode_literals

import csv
import os
import re

from os.path import dirname, join as pjoin

from twilio.rest import TwilioRestClient


def send_sms(message):
    account = os.environ['TWILIO_SID']
    token = os.environ['TWILIO_AUTH_TOKEN']
    from_number = os.environ['TWILIO_FROM_NUMBER']
    dry_run = os.environ.get('DRY_RUN', 'false') == 'true'

    client = TwilioRestClient(account=account, token=token)

    for recipient in get_recipients():
        if dry_run:
            print("Dry run, skipping {}".format(recipient))
            continue

        client.messages.create(
            from_=from_number,
            to=recipient,
            body=message
        )


def get_recipients():
    filename = pjoin(dirname(__file__), '..', 'recipients.csv')
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['enabled'] != 'true':
                continue

            mobile_number = row['mobile_number']
            if not valid_mobile_number(mobile_number):
                print("ERROR: Bad mobile number '{}'".format(mobile_number))
                continue

            print("{} ({}): {}".format(
                row['name'],
                row['paypal_email'],
                mobile_number))

            yield mobile_number


def valid_mobile_number(mobile_number):
    """
    >>> valid_mobile_number('+447987123765')
    True
    >>> valid_mobile_number('+44798712376')
    False
    >>> valid_mobile_number('+4479871237657')
    False
    """
    match = re.match(r'^\+447\d{9}$', mobile_number)
    return match is not None
