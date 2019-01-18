import csv
import sys

from datetime import datetime
from sets import Set

from market import Period
from quote_source import QuoteSource

date_format = "%Y-%m-%d"


def load_data_from_csv(symbol):
    data_path = 'market/yahoo/'
    file = data_path + symbol + '.csv'
    quotes = []
    try:
        with open(file, 'r') as data:
            reader = csv.reader(data)
            next(reader, None)
            for row in reader:
                if not row:
                    continue
                quote = {}
                quote['symbol'] = symbol
                try:
                    quote['datetime'] = datetime.strptime(
                        row[0], "%Y-%m-%d")
                    row_base = 1
                    real_close = float(row[row_base + 3])
                    adj_close = float(row[row_base + 4])
                    adj_ratio = adj_close / real_close;
                    quote['open'] = float(row[row_base]) * adj_ratio
                    quote['high'] = float(row[row_base + 1]) * adj_ratio
                    quote['low'] = float(row[row_base + 2]) * adj_ratio
                    quote['close'] = adj_close
                    quote['volume'] = int(row[row_base + 5])
                except ValueError:
                    continue
                quotes.append(quote)
    except EnvironmentError:
        print("%s not found. Please download the csv from "
              "https://finance.yahoo.com/quote/%s/history" % (
                  file, symbol))
        sys.exit(-1)
    return quotes


class YahooQuoteSource(QuoteSource):
    def __init__(self):
        self._loaded_map = {}
        self._quote_map = {}
        self._loaded_symbol = Set()

    def load_data(self, symbol_list, start_datetime, end_datetime):
        unloaded_symbol_set = Set(symbol_list).difference(self._loaded_symbol)
        for symbol in unloaded_symbol_set:
            quotes = load_data_from_csv(symbol)
            for quote in quotes:
                self._loaded_map.setdefault(
                    quote['datetime'], []).append(quote)

        self._loaded_symbol.update(Set(symbol_list))

        for loaded_datetime in self._loaded_map:
            if start_datetime <= loaded_datetime <= end_datetime:
                self._quote_map[loaded_datetime] = \
                    self._loaded_map[loaded_datetime]

    def get_symbol_data(self, symbol):
        return load_data_from_csv(symbol)

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
