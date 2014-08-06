from __future__ import unicode_literals

import datetime
import pytz

import lxml.etree

from .two_hourly_forecast import TwoHourlyForecast


"""
The Norwegian weather service API 1.9 returns a pretty cool data format, albeit
encoded in XML. It contains two types of forecasts:

    1. point-in-time (from="2014-08-03T19:00:00Z" to="2014-08-03T19:00:00Z")
    2. range         (from="2014-08-03T18:00:00Z" to="2014-08-03T19:00:00Z"

The point-in-time forecasts it gives lots of data like this:

    <temperature id="TTT" unit="celsius" value="15.5"/>
    <windDirection id="dd" deg="217.1" name="SW"/>
    <windSpeed id="ff" mps="4.2" beaufort="3" name="Lett bris"/>
    <humidity value="76.0" unit="percent"/>
    <pressure id="pr" unit="hPa" value="1010.7"/>
    <cloudiness id="NN" percent="17.7"/>
    <fog id="FOG" percent="0.0"/>
    <lowClouds id="LOW" percent="17.7"/>
    <mediumClouds id="MEDIUM" percent="0.0"/>
    <highClouds id="HIGH" percent="0.0"/>
    <dewpointTemperature id="TD" unit="celsius" value="11.4"/>

Whereas for ranges it just gives:

    <precipitation unit="mm" value="0.0" minvalue="0.0" maxvalue="0.0"/>
    <symbol id="LightCloud" number="2"/>

For your convenience, it seems, 1, 2, 3, 4 and 6 hour ranges are available.

"""


def get_two_hourly_forecasts(xml_f, utc_startfrom, timezone, count):
    root = lxml.etree.fromstring(xml_f.read())
    point_time_forecasts = parse_point_time_forecasts(root)
    two_hour_range_forecasts = parse_two_hour_range_forecasts(root)

    for hour_offset in range(0, count * 2, 2):
        forecast_time = utc_startfrom + datetime.timedelta(hours=hour_offset)

        temperature = parse_temperature(point_time_forecasts[forecast_time])

        min_rain, max_rain = parse_precipitation(
            two_hour_range_forecasts[forecast_time])

        yield make_two_hourly_forecast(forecast_time, timezone, temperature,
                                       min_rain, max_rain)


def parse_point_time_forecasts(lxml):
    result = {}
    xpath = '//weatherdata/product[@class="pointData"]/time[@from=@to]'
    for node in lxml.xpath(xpath):
        result[parse_datetime(node.get('from'))] = node
    return result


def parse_two_hour_range_forecasts(lxml):
    result = {}
    xpath = '//weatherdata/product[@class="pointData"]/time[@from]'
    for node in lxml.xpath(xpath):
        from_ = parse_datetime(node.get('from'))
        to = parse_datetime(node.get('to'))
        if to - from_ == datetime.timedelta(hours=2):
            result[from_] = node
    return result


def parse_datetime(string):
    return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ').replace(
        tzinfo=pytz.UTC)


def parse_temperature(time_node):
    temp = time_node.xpath('./location/temperature[@unit="celsius"]/@value')[0]
    return float(temp)


def parse_precipitation(time_node):
    min_ = time_node.xpath('./location/precipitation[@unit="mm"]/@minvalue')[0]
    max_ = time_node.xpath('./location/precipitation[@unit="mm"]/@maxvalue')[0]
    return float(min_), float(max_)


def make_two_hourly_forecast(utc_time, timezone, temperature, min_rain,
                             max_rain):
    return TwoHourlyForecast(
        start_datetime=utc_time.astimezone(pytz.timezone(timezone)),
        temperature=temperature,
        min_rain=min_rain,
        max_rain=max_rain)
