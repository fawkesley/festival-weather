from __future__ import unicode_literals

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO  # Python 2 compat

import datetime
import logging

import pytz
# import backoff
import requests

# from requests.exceptions import RequestException

from .parser import get_two_hourly_forecasts

URL = ('http://api.yr.no/weatherapi/locationforecast/1.9/'
       '?lat={latitude};lon={longitude};msl={altitude}')


def download_latest_forecasts(lat, lng, altitude, timezone, count=8):
    utc_nowish = get_next_even_hour_for_timezone(timezone)

    url = URL.format(latitude=lat, longitude=lng, altitude=altitude)
    xml_f = get_url(url)

    return list(get_two_hourly_forecasts(xml_f, utc_nowish, timezone, count))


def get_next_even_hour_for_timezone(timezone):
    """
    Given a timezone ie Europe/London, return the most recent nicely rounded
    even hour like 8am, 10am.
    Return it in UTC format!
    """
    now = (datetime.datetime.now(pytz.timezone(timezone))
           + datetime.timedelta(hours=1)).replace(
               second=0, minute=0, microsecond=0)

    is_odd = lambda x: x % 2 != 0
    if is_odd(now.hour):
        now = now + datetime.timedelta(hours=1)

    return now.astimezone(pytz.UTC)


# @backoff.on_exception(backoff.expo, RequestException, max_tries=4)
def get_url(url):
    logging.debug("Downloading {}".format(url))
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)
