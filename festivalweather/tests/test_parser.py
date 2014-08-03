# encoding: utf-8

from __future__ import unicode_literals

import datetime
import unittest

from os.path import dirname, join as pjoin

import pytz

from nose.tools import assert_equal

from ..two_hourly_forecast import TwoHourlyForecast
from ..parser import get_two_hourly_forecasts


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utc_start = datetime.datetime(2014, 8, 3, 21, 0, 0, tzinfo=pytz.UTC)
        with open(pjoin(dirname(__file__), 'sample_forecast.xml')) as f:
            cls.forecasts = list(
                get_two_hourly_forecasts(f, utc_start, 'Europe/London', 8))

    def test_that_eight_forecasts_are_returned(self):
        assert_equal(8, len(self.forecasts))

    def test_that_temperatures_are_correct(self):
        assert_equal(
            [0, 0, 0, 0, 0, 0, 0, 0],
            [f.temperature for f in self.forecasts])

    def test_that_min_precipitations_are_correct(self):
        assert_equal(
            [0, 0, 0, 0, 0, 0, 0, 0],
            [f.min_rain for f in self.forecasts])

    def test_that_max_precipitations_are_correct(self):
        assert_equal(
            [0, 0, 0, 0, 0, 0, 0, 0],
            [f.max_rain for f in self.forecasts])

    def test_that_start_datetimes_all_have_london_timezone(self):
        assert_equal(
            set([pytz.timezone('Europe/London').zone]),
            set([f.start_datetime.tzinfo.zone for f in self.forecasts]))

    def test_that_start_datetimes_are_all_correct(self):
        self.maxDiff = None
        tz = pytz.timezone('Europe/London')
        assert_equal(
            [datetime.datetime(2014, 8, 3, 22, 0, 0, tzinfo=tz)],
            [f.start_datetime for f in self.forecasts])
