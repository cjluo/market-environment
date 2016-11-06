from enum import Enum


class Period(Enum):
    day = 1
    hour = 2
    minute = 3


class Action(Enum):
    buy = 1
    sell = 2
    hold = 3


class Market(object):
    def __init__(self, quote_source, order_cost):
        self._quote_source = quote_source
        self._order_cost = order_cost

    def load_data(self, symbol_list, start_datetime, end_datetime):
        self._quote_source.load_data(symbol_list, start_datetime, end_datetime)

    def get_quote_map(self, datetime, period):
        return self._quote_source.get_quote_map(datetime, period)

    def execute_order_list(self, order_list, datetime, period):
        quote_map = self.get_quote_map(datetime, period)

        cash = 0
        execute_order_list = []
        for order in order_list:
            if order['symbol'] in quote_map:
                quote = quote_map[order['symbol']]
                order_executed = False
                if (order['action'] == Action.buy and
                        order['price'] > quote['low']):
                    order_executed = True

                if (order['action'] == Action.sell and
                        order['price'] < quote['high']):
                    order_executed = True

                if order_executed:
                    execute_order_list.append(order)
                    if order['action'] == Action.buy:
                        cash -= order['price'] * order['amount'] \
                            + self._order_cost
                    else:
                        cash += order['price'] * order['amount'] \
                            - self._order_cost

        return execute_order_list, cash

    def get_datetime_list(self, period):
        return sorted(self._quote_source.get_datetime_list(period))
