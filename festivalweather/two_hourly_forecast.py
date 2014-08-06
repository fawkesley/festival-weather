# encoding: utf-8

from __future__ import unicode_literals

from collections import namedtuple


class TwoHourlyForecast(namedtuple('TwoHourlyForecast',
                                   'start_datetime,temperature,'
                                   'min_rain,max_rain')):
    """
    A forecast for a two-hour period at a particular location. Note that the
    start_datetime must have the timezone for this period.
    """

    def __init__(self, *args, **kwargs):
        super(TwoHourlyForecast, self).__init__(*args, **kwargs)
        if self.start_datetime.tzinfo is None:
            raise ValueError("start_datetime must be timezone-aware and should"
                             "have the timezone of the forecast location.")

        float(self.temperature)
        float(self.min_rain)
        float(self.max_rain)

    def __str__(self):
        return '{time} {temp} {rain}'.format(
            time=self.get_time_string(),
            temp=self.get_temperature_string(),
            rain=self.get_precipitation_string())

    def get_time_string(self):
        return self.start_datetime.strftime('%I%P').lstrip('0')

    def get_temperature_string(self):
        return '{:.0f}º'.format(self.temperature)

    def get_precipitation_string(self):
        if self.max_rain == 0.0:
            return 'dry'
        elif self.min_rain == self.max_rain:
            return '{:.1f}mm'.format(round(self.min_rain, 1))
        else:
            return '{:.1f}-{:.1f}mm'.format(
                round(self.min_rain, 1),
                round(self.max_rain, 1))
