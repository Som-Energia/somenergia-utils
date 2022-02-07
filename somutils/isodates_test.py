#!/usr/bin/env python

from .isodates import (
    asUtc,
    toLocal,
    parseLocalTime,
    assertLocalDateTime,
    daterange,
    isodate,
    addHours,
    addDays,
    )

import datetime

import unittest

def localTime(string):
    isSummer = string.endswith("S")
    if isSummer: string=string[:-1]
    return parseLocalTime(string, isSummer)

class LocalTime_Test(unittest.TestCase):

    def test_localTime_fullySummer(self):
        self.assertEqual(
            str(localTime("2016-08-15 02:00:00")),
            "2016-08-15 02:00:00+02:00")

    def test_localTime_fullyWinter(self):
        self.assertEqual(
            str(localTime("2016-01-01 02:10:00")),
            "2016-01-01 02:10:00+01:00")

    def test_localTime_badTz_ignored(self):
        self.assertEqual(
            str(localTime("2016-01-01 02:00:00S")),
            "2016-01-01 02:00:00+01:00")

    def test_localTime_badSummerTz_ignored(self):
        self.assertEqual(
            str(localTime("2016-08-15 02:00:00")),
            "2016-08-15 02:00:00+02:00")

    def test_localTime_beforeOctoberChange(self):
        self.assertEqual(
            str(localTime("2016-10-30 02:00:00S")),
            "2016-10-30 02:00:00+02:00")

    def test_localTime_afterOctoberChange(self):
        self.assertEqual(
            str(localTime("2016-10-30 02:00:00")),
            "2016-10-30 02:00:00+01:00")

    def test_localTime_SIgnored(self):
        self.assertEqual(
            str(localTime("2016-10-30 03:00:00S")),
            "2016-10-30 03:00:00+01:00")

    @unittest.skip('toreview: it should fail')
    def test_localTime_unexistingHour(self):
        self.assertEqual(
            str(localTime("2016-03-27 02:00:00")),
            "2016-03-27 02:00:00+01:00")

    def test_localTime_atWinterMidnight(self):
        self.assertEqual(
            str(localTime("2016-01-01 00:00:00")),
            "2016-01-01 00:00:00+01:00")

    def test_assertLocalDateTime_withDate(self):
        with self.assertRaises(AssertionError) as ctx:
            assertLocalDateTime('myname', datetime.date(2016,1,1))
        self.assertEqual(ctx.exception.args[0],
            "myname should be a datetime")

    def test_assertLocalDateTime_withNaive(self):
        with self.assertRaises(AssertionError) as ctx:
            assertLocalDateTime('myname', datetime.datetime(2016,1,1))
        self.assertEqual(ctx.exception.args[0],
            "myname should have timezone")

    def test_assertLocalDateTime_withUTC(self):
        with self.assertRaises(AssertionError) as ctx:
            assertLocalDateTime('myname', asUtc(datetime.datetime(2016,1,1)))
        self.assertEqual(ctx.exception.args[0],
            "myname has UTC timezone")

    def test_assertLocalDateTime_withLocal(self):
        assertLocalDateTime('myname', toLocal(datetime.datetime(2016,1,1)))
        # No assert

    def test_daterange(self):
        days = daterange(
            isodate('2020-01-02'),
            isodate('2020-01-04'),
        )
        self.assertEqual(list(days), [
            isodate('2020-01-02'),
            isodate('2020-01-03'),
            isodate('2020-01-04'),
        ])

    def test_daterange_invertedRange(self):
        days = daterange(
            isodate('2020-01-04'),
            isodate('2020-01-02'),
        )
        self.assertEqual(list(days), [
        ])





# vim: et ts=4 sw=4
