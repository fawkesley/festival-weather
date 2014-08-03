# encoding: utf-8

from __future__ import unicode_literals

import datetime
import unittest

import pytz

from nose.tools import assert_equal, assert_raises

from ..two_hourly_forecast import TwoHourlyForecast


class TestForecastBase(unittest.TestCase):
    utc_datetime = datetime.datetime(2014, 6, 1, 9, 0, 0, tzinfo=pytz.UTC)


class TestConstructor(TestForecastBase):
    def test_that_naive_datetimes_cause_value_error(self):
        naive_datetime = datetime.datetime(2014, 6, 1, 0, 0, 0)
        assert_raises(
            ValueError,
            lambda: TwoHourlyForecast(
                start_datetime=naive_datetime,
                temperature=18.0, min_rain=0.0, max_rain=0.0))

    def test_that_utc_datetimes_dont_raise_value_error(self):
        TwoHourlyForecast(
            start_datetime=self.utc_datetime,
            temperature=18.0, min_rain=0.0, max_rain=0.0)


class TestGetTimeString(TestForecastBase):
    def test_that_time_is_displayed_in_correct_timezone(self):
        uk_datetime = self.utc_datetime.astimezone(
            pytz.timezone('Europe/London'))

        forecast = TwoHourlyForecast(
            start_datetime=uk_datetime,
            temperature=18.0, min_rain=0, max_rain=0)

        assert_equal('10am', forecast.get_time_string())


class TestGetTemperatureString(TestForecastBase):
    def test_that_temperature_has_no_decimal_places(self):
        forecast = TwoHourlyForecast(
            start_datetime=self.utc_datetime,
            temperature=18.6, min_rain=0, max_rain=0)

        assert_equal('19º', forecast.get_temperature_string())


class TestGetPrecipitationString(TestForecastBase):
    def test_that_no_max_rain_reads_as_dry(self):
        forecast = TwoHourlyForecast(
            start_datetime=self.utc_datetime,
            temperature=18.6, min_rain=0, max_rain=0)

        assert_equal('dry', forecast.get_precipitation_string())

    def test_that_precipitation_range_have_1_decimal_place(self):
        forecast = TwoHourlyForecast(
            start_datetime=self.utc_datetime,
            temperature=18.6, min_rain=0.56, max_rain=0.72)

        assert_equal('0.6-0.7mm', forecast.get_precipitation_string())

    def test_that_025_is_rounded_correctly(self):
        forecast = TwoHourlyForecast(
            start_datetime=self.utc_datetime,
            temperature=18.6, min_rain=0.25, max_rain=0.72)

        assert_equal('0.3-0.7mm', forecast.get_precipitation_string())


class TestUnicodeMethod(TestForecastBase):
    def test_that_python_3_str_method_gives_correct_string(self):
        forecast = TwoHourlyForecast(
            start_datetime=self.utc_datetime,
            temperature=18.6, min_rain=0.25, max_rain=1.34)
        assert_equal('9am 19º 0.3-1.3mm', forecast.__str__())
