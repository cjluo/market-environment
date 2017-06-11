from datetime import datetime
import unittest

from yahoo_quote_source import YahooQuoteSource
from market import Period


class LoadData(unittest.TestCase):
    def setUp(self):
        self._quote_source = YahooQuoteSource()
        self._quote_source.load_data(['TWTR', 'GOOG'],
                                     datetime(2016, 1, 1, 1, 1, 1),
                                     datetime(2016, 2, 2, 2, 2, 2))
        self._quote_source.load_data(['TWTR', 'GOOG'],
                                     datetime(2013, 1, 1, 1, 1, 1),
                                     datetime(2013, 2, 2, 2, 2, 2))

    def test_correct_data(self):
        quotes = self._quote_source.get_quote_map(
            datetime(2016, 2, 1, 1, 1, 1), Period.day)

        quotes_expected = (
            "{'GOOG': {'volume': 5139200, 'symbol': 'GOOG', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 757.859985, 'low': "
            "743.27002, 'close': 752.0, 'open': 750.460022}, 'TWTR': "
            "{'volume': 49994400, 'symbol': 'TWTR', 'datetime': "
            "datetime.datetime(2016, 2, 1, 0, 0), 'high': 18.77, 'low': "
            "17.299999, 'close': 17.91, 'open': 17.889999}}")

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
            "{'GOOG': {'volume': 7520100, 'symbol': 'GOOG', 'datetime': "
            "datetime.datetime(2013, 2, 1, 0, 0), 'high': 386.850006, "
            "'low': 377.634521, 'close': 773.476501, 'open': 377.684357}}")

        self.assertEqual(quotes_expected, str(quotes))

    def test_datetime_list(self):
        self.assertEqual(
            43, len(self._quote_source.get_datetime_list(Period.day)))

    def test_load_single_quote(self):
        self.assertEqual(
            "{'volume': 44871300, 'symbol': 'GOOG', 'datetime': "
            "datetime.datetime(2004, 8, 19, 0, 0), 'high': 51.835709, "
            "'low': 47.800831, 'close': 100.065277, 'open': 49.813286}", str(
                self._quote_source.get_symbol_data('GOOG')[0]))


if __name__ == '__main__':
    unittest.main()
