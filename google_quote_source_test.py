from datetime import datetime
import unittest

from google_quote_source import GoogleQuoteSource
from market import Period


class LoadData(unittest.TestCase):
    def setUp(self):
        self._quote_source = GoogleQuoteSource()
        self._quote_source.load_data(['AAPL', 'TWTR'],
                                     datetime(2016, 1, 1, 1, 1, 1),
                                     datetime(2016, 2, 2, 2, 2, 2))
        self._quote_source.load_data(['AAPL', 'TWTR'],
                                     datetime(2013, 1, 1, 1, 1, 1),
                                     datetime(2013, 2, 2, 2, 2, 2))

    def test_correct_data(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 2, 1, 1, 1, 1), Period.day)

        quotes_expected = (
            "{'TWTR': {'volume': 49875496, 'symbol': 'TWTR', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 18.77, 'low': 17.3, "
            "'close': 17.91, 'open': 17.89}, 'AAPL': {'volume': 40571593, "
            "'symbol': 'AAPL', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 96.71, 'low': 95.4, "
            "'close': 96.43, 'open': 96.47}}")

        self.assertEqual(quotes_expected, str(quotes))

    def test_empty_data(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 1, 30, 1, 1, 1), Period.day)

        quotes_expected = "{}"

        self.assertEqual(quotes_expected, str(quotes))

    def test_old_data(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2013, 2, 1, 1, 1, 1), Period.day)

        quotes_expected = (
            "{'AAPL': {'volume': 134867089, 'symbol': 'AAPL', 'datetime': "
            "datetime.datetime(2013, 2, 1, 0, 0), 'high': 65.64, 'low': "
            "64.05, 'close': 64.8, 'open': 65.59}}")

        self.assertEqual(quotes_expected, str(quotes))

    def test_datetime_list(self):
        self.assertEqual(
            43, len(self._quote_source.get_datetime_list(Period.day)))


if __name__ == '__main__':
    unittest.main()
