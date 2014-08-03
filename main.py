#!/usr/bin/env python

from festivalweather import download_latest_forecasts, send_sms

if __name__ == '__main__':
    import os

    forecasts = download_latest_forecasts(
        os.environ['LOCATION_LATITUDE'],
        os.environ['LOCATION_LONGITUDE'],
        os.environ['LOCATION_ALTITUDE'],
        os.environ['LOCATION_TIMEZONE'])
    message = '\n'.join(['{}'.format(f) for f in forecasts])
    print(message)
    print("Sending SMS...")
    send_sms(message)
    print("Done.")
