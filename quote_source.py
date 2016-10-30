class QuoteSource:
    def load_data(self, symbol_list, start_datetime, end_datetime):
        raise NotImplementedError

    def get_quote_map(self, symbol_list, start_datetime, end_datetime):
        raise NotImplementedError
