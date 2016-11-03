from datetime import datetime
import unittest

from stooq_quote_source import StooqQuoteSource
from market import Period


class LoadData(unittest.TestCase):
    def setUp(self):
        self._quote_source = StooqQuoteSource()
        self._quote_source.load_data(['TWTR', 'AAPL'],
                                     datetime(2016, 10, 1, 1, 1, 1),
                                     datetime(2016, 10, 4, 2, 2, 2))
        self._quote_source.load_data(['TWTR', 'AAPL'],
                                     datetime(2016, 1, 1, 1, 1, 1),
                                     datetime(2016, 2, 2, 2, 2, 2))
        self._quote_source.load_data(['TWTR', 'AAPL'],
                                     datetime(2013, 1, 1, 1, 1, 1),
                                     datetime(2013, 2, 2, 2, 2, 2))

    def test_correct_data_day(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 2, 1, 1, 1, 1), Period.day)

        quotes_expected = (
            "{'TWTR': {'volume': 49950388, 'symbol': 'TWTR', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 18.8, 'low': 17.3, "
            "'close': 17.91, 'open': 17.89}, 'AAPL': {'volume': 39111557, "
            "'symbol': 'AAPL', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 95.091, 'low': "
            "93.803, 'close': 94.816, 'open': 94.854}}")

        self.assertEqual(quotes_expected, str(quotes))

    def test_old_data_day(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2013, 2, 1, 1, 1, 1), Period.day)

        quotes_expected = (
            "{'AAPL': {'volume': 145969156, 'symbol': 'AAPL', 'datetime': "
            "datetime.datetime(2013, 2, 1, 0, 0), 'high': 60.629, 'low': "
            "59.159, 'close': 59.856, 'open': 60.58}}")

        self.assertEqual(quotes_expected, str(quotes))

    def test_correct_data_hour(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 10, 3, 13, 1, 1), Period.hour)

        quotes_expected = (
            "{'TWTR': {'volume': 2808671, 'symbol': 'TWTR', 'datetime': "
            "datetime.datetime(2016, 10, 3, 13, 0), 'high': 23.89, 'low': "
            "23.61, 'close': 23.875, 'open': 23.6817}, 'AAPL': {'volume': "
            "1905609, 'symbol': 'AAPL', 'datetime': datetime.datetime(2016, "
            "10, 3, 13, 0), 'high': 112.64, 'low': 112.36, 'close': 112.37, "
            "'open': 112.61}}")

        self.assertEqual(quotes_expected, str(quotes))

    def test_empty_data(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 1, 30, 1, 1, 1), Period.day)

        quotes_expected = "{}"

        self.assertEqual(quotes_expected, str(quotes))

    def test_datetime_list(self):
        self.assertEqual(
            45, len(self._quote_source.get_datetime_list(Period.day)))
        self.assertEqual(
            7, len(self._quote_source.get_datetime_list(Period.hour)))


if __name__ == '__main__':
    unittest.main()
