import csv
import urllib2

from datetime import datetime
from sets import Set

from market import Period
from quote_source import QuoteSource

date_format = "%Y-%m-%d"


class YahooQuoteSource(QuoteSource):
    def __init__(self):
        self._loaded_map = {}
        self._quote_map = {}
        self._loaded_symbol = Set()

    def load_data(self, symbol_list, start_datetime, end_datetime):
        unloaded_symbol_set = Set(symbol_list).difference(self._loaded_symbol)
        for symbol in unloaded_symbol_set:
            response = urllib2.urlopen(
                'http://ichart.finance.yahoo.com/table.csv?s=%s' % symbol)
            reader = csv.reader(response)
            next(reader, None)
            for row in reader:
                quote = {}
                quote['symbol'] = symbol
                quote['datetime'] = datetime.strptime(row[0], date_format)

                split_ratio = float(row[6]) / float(row[4])

                quote['open'] = float(
                    format(float(row[1]) * split_ratio, '.2f'))
                quote['high'] = float(
                    format(float(row[2]) * split_ratio, '.2f'))
                quote['low'] = float(
                    format(float(row[3]) * split_ratio, '.2f'))
                quote['close'] = float(
                    format(float(row[4]) * split_ratio, '.2f'))
                quote['volume'] = int(row[5])
                self._loaded_map.setdefault(
                    quote['datetime'], []).append(quote)

        self._loaded_symbol.update(Set(symbol_list))

        for loaded_datetime in self._loaded_map:
            if start_datetime <= loaded_datetime <= end_datetime:
                self._quote_map[loaded_datetime] = \
                    self._loaded_map[loaded_datetime]

    def get_quote_map(self, quote_datetime, period):
        if period != Period.day:
            raise NotImplementedError

        quote_date = quote_datetime.date()
        quote_datetime = datetime(
            quote_date.year, quote_date.month, quote_date.day)
        if quote_datetime not in self._quote_map:
            return {}
        quotes = self._quote_map[quote_datetime]
        symbol_map = {}
        for quote in quotes:
            symbol_map[quote['symbol']] = quote

        return symbol_map

    def get_datetime_list(self, period):
        if period != Period.day:
            raise NotImplementedError
        return self._quote_map.keys()
