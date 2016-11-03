class QuoteSource:
    def load_data(self, symbol_list, start_datetime, end_datetime):
        raise NotImplementedError

    def get_quote_map(self, quote_datetime, period):
        raise NotImplementedError

    def get_datetime_list(self, period):
        raise NotImplementedError
