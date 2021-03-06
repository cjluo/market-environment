import csv
import urllib2

from datetime import datetime

from market import Period
from quote_source import QuoteSource

date_format = "%b+%d+%Y"


class GoogleQuoteSource(QuoteSource):
    def __init__(self):
        self._quote_map = {}

    def load_data(self, symbol_list, start_datetime, end_datetime):
        for symbol in symbol_list:

            url = (
                'http://www.google.com/finance/historical'
                '?q=%s&histperiod=daily&startdate=%s&enddate=%s'
                '&output=csv') % (
                    symbol,
                    start_datetime.strftime(date_format),
                    end_datetime.strftime(date_format))
            print "%s: %s" % (symbol, url)

            response = urllib2.urlopen(url)
            reader = csv.reader(response)
            next(reader, None)
            for row in reader:
                quote = {}
                quote['symbol'] = symbol
                quote['datetime'] = datetime.strptime(row[0], "%d-%b-%y")
                if row[1] == '-':
                    continue
                quote['open'] = float(row[1])
                if row[2] == '-':
                    continue
                quote['high'] = float(row[2])
                if row[3] == '-':
                    continue
                quote['low'] = float(row[3])
                if row[4] == '-':
                    continue
                quote['close'] = float(row[4])
                if row[5] == '-':
                    quote['volume'] = 0
                else:
                    quote['volume'] = int(row[5])
                self._quote_map.setdefault(quote['datetime'], []).append(quote)

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
