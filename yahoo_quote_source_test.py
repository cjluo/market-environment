from datetime import datetime
import unittest

from yahoo_quote_source import YahooQuoteSource
from market import Period


class LoadData(unittest.TestCase):
    def setUp(self):
        self._quote_source = YahooQuoteSource()
        self._quote_source.load_data(['TWTR', 'AAPL'],
                                     datetime(2016, 1, 1, 1, 1, 1),
                                     datetime(2016, 2, 2, 2, 2, 2))
        self._quote_source.load_data(['TWTR', 'AAPL'],
                                     datetime(2013, 1, 1, 1, 1, 1),
                                     datetime(2013, 2, 2, 2, 2, 2))

    def test_correct_data(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 2, 1, 1, 1, 1), Period.day)

        quotes_expected = (
            "{'TWTR': {'volume': 49994400, 'symbol': 'TWTR', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 18.77, 'low': 17.3, "
            "'close': 17.91, 'open': 17.89}, 'AAPL': {'volume': 40943500, "
            "'symbol': 'AAPL', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 95.09, 'low': 93.8, "
            "'close': 94.82, 'open': 94.85}}")

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
            "{'AAPL': {'volume': 134871100, 'symbol': 'AAPL', 'datetime': "
            "datetime.datetime(2013, 2, 1, 0, 0), 'high': 60.63, 'low': "
            "59.16, 'close': 59.86, 'open': 60.58}}")

        self.assertEqual(quotes_expected, str(quotes))


if __name__ == '__main__':
    unittest.main()
