import csv
import os

from datetime import datetime, timedelta
from sets import Set
from zipfile import ZipFile

from market import Period
from quote_source import QuoteSource


class StooqQuoteSource(QuoteSource):
    """Data downloaded from https://stooq.com/db/h/ and saved in stooq/"""
    def __init__(self):
        self._loaded_map = {Period.day: {}, Period.hour: {}}
        self._quote_map = {Period.day: {}, Period.hour: {}}
        self._loaded_symbol = Set()

    def load_data(self, symbol_list, start_datetime, end_datetime):
        unloaded_symbol_set = Set(symbol_list).difference(self._loaded_symbol)
        self.__load_data(unloaded_symbol_set, Period.day)
        self.__load_data(unloaded_symbol_set, Period.hour)
        self._loaded_symbol.update(Set(symbol_list))

        for period in [Period.day, Period.hour]:
            for loaded_datetime in self._loaded_map[period]:
                if start_datetime <= loaded_datetime <= end_datetime:
                    self._quote_map[period][loaded_datetime] = \
                        self._loaded_map[period][loaded_datetime]

    def __load_data(self, symbol_list, period):
        if period == Period.day:
            data_asset = 'stooq/d_us_txt.zip'
        elif period == Period.hour:
            data_asset = 'stooq/h_us_txt.zip'
        else:
            raise NotImplementedError

        with ZipFile(data_asset, 'r') as data:
            filepaths = data.namelist()
            filenames = [os.path.basename(
                path).split('.')[0].upper() for path in filepaths]

            symbol_map = dict(zip(filenames, filepaths))

            for symbol in symbol_list:
                file = symbol_map[symbol]
                reader = csv.reader(data.read(file).split('\n'))
                next(reader, None)
                for row in reader:
                    if not row:
                        continue
                    quote = {}
                    quote['symbol'] = symbol
                    if period == Period.day:
                        quote['datetime'] = datetime.strptime(row[0], "%Y%m%d")
                        row_base = 1
                    elif period == Period.hour:
                        quote['datetime'] = datetime.strptime(
                            row[0] + row[1], "%Y-%m-%d%H:%M:%S") - timedelta(
                            hours=7)  # converts to EST timezon
                        row_base = 2
                    quote['open'] = float(row[row_base])
                    quote['high'] = float(row[row_base + 1])
                    quote['low'] = float(row[row_base + 2])
                    quote['close'] = float(row[row_base + 3])
                    quote['volume'] = int(row[row_base + 4])
                    self._loaded_map[period].setdefault(
                        quote['datetime'], []).append(quote)

    def get_quote_map(self, quote_datetime, period):
        if period == Period.day:
            quote_date = quote_datetime.date()
            quote_datetime = datetime(
                quote_date.year, quote_date.month, quote_date.day)
        elif period == Period.hour:
            quote_datetime = datetime(
                quote_datetime.year,
                quote_datetime.month,
                quote_datetime.day,
                quote_datetime.hour)
        else:
            raise NotImplementedError

        if quote_datetime not in self._quote_map[period]:
            return {}
        quotes = self._quote_map[period][quote_datetime]
        symbol_map = {}
        for quote in quotes:
            symbol_map[quote['symbol']] = quote

        return symbol_map

    def get_datetime_list(self, period):
        return self._quote_map[period].keys()
