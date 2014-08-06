# encoding: utf-8

from __future__ import unicode_literals

import datetime
import unittest

from os.path import dirname, join as pjoin

import pytz

from nose.tools import assert_equal

from ..parser import get_two_hourly_forecasts


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.utc_start = datetime.datetime(2014, 8, 3, 21, 0, 0,
                                          tzinfo=pytz.UTC)
        with open(pjoin(dirname(__file__), 'sample_forecast.xml')) as f:
            cls.forecasts = list(
                get_two_hourly_forecasts(f, cls.utc_start, 'Europe/London', 8))

    def test_that_eight_forecasts_are_returned(self):
        assert_equal(8, len(self.forecasts))

    def test_that_temperatures_are_correct(self):
        assert_equal(
            [15.2, 14.3, 12.6, 11.6, 10.9, 13.0, 16.9, 17.9],
            [f.temperature for f in self.forecasts])

    def test_that_min_precipitations_are_correct(self):
        assert_equal(
            [1.6, 8.4, 0, 0, 0, 0, 0, 0.1],
            [f.min_rain for f in self.forecasts])

    def test_that_max_precipitations_are_correct(self):
        assert_equal(
            [3.8, 9.6, 0.0, 0.0, 0.0, 0.1, 0.5, 0.6],
            [f.max_rain for f in self.forecasts])

    def test_that_start_datetimes_all_have_london_timezone(self):
        assert_equal(
            set([pytz.timezone('Europe/London').zone]),
            set([f.start_datetime.tzinfo.zone for f in self.forecasts]))

    @staticmethod
    def _to_london(datetime):
        return datetime.astimezone(pytz.timezone('Europe/London'))

    def test_that_start_datetimes_are_all_correct(self):
        self.maxDiff = None
        expected_datetimes = []
        for hour in (0, 2, 4, 6, 8, 10, 12, 14):
            expected_datetimes.append(
                self._to_london(
                    self.utc_start + datetime.timedelta(hours=hour)))

        assert_equal(
            expected_datetimes,
            [f.start_datetime for f in self.forecasts])
