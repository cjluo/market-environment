from datetime import datetime
import unittest

from google_quote_source import GoogleQuoteSource
from stooq_quote_source import StooqQuoteSource
from yahoo_quote_source import YahooQuoteSource
from market import Action, Market, Period


class ExecuteOrder(unittest.TestCase):
    def setUp(self):
        self._order_cost = 5

    def test_google_quote_source(self):
        market = Market(GoogleQuoteSource(), self._order_cost)
        market.load_data(
            ['GOOG', 'TWTR'],
            datetime(2013, 1, 1),
            datetime(2016, 1, 1))

        success_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 1000}]
        executed_order_list, cash = market.execute_order_list(
            success_buy_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual(success_buy_list, executed_order_list)
        self.assertEqual(-1005, cash)

        success_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            success_sell_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual(success_sell_list, executed_order_list)
        self.assertEqual(95, cash)

        failing_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 510}]
        executed_order_list, cash = market.execute_order_list(
            failing_buy_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 530}]
        executed_order_list, cash = market.execute_order_list(
            failing_sell_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_order_list_not_exist = [{
            'symbol': 'TWTR',
            'action': Action.buy,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            failing_order_list_not_exist, datetime(2013, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

    def test_yahoo_quote_source(self):
        market = Market(YahooQuoteSource(), self._order_cost)
        market.load_data(
            ['GOOG', 'TWTR'],
            datetime(2013, 1, 1),
            datetime(2016, 1, 1))

        success_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 1000}]
        executed_order_list, cash = market.execute_order_list(
            success_buy_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual(success_buy_list, executed_order_list)
        self.assertEqual(-1005, cash)

        success_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            success_sell_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual(success_sell_list, executed_order_list)
        self.assertEqual(95, cash)

        failing_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 510}]
        executed_order_list, cash = market.execute_order_list(
            failing_buy_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 530}]
        executed_order_list, cash = market.execute_order_list(
            failing_sell_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_order_list_not_exist = [{
            'symbol': 'TWTR',
            'action': Action.buy,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            failing_order_list_not_exist, datetime(2013, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

    def test_stooq_quote_source_day(self):
        market = Market(StooqQuoteSource(), self._order_cost)
        market.load_data(
            ['GOOG', 'TWTR'],
            datetime(2013, 1, 1),
            datetime(2016, 1, 1))

        success_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 1000}]
        executed_order_list, cash = market.execute_order_list(
            success_buy_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual(success_buy_list, executed_order_list)
        self.assertEqual(-1005, cash)

        success_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            success_sell_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual(success_sell_list, executed_order_list)
        self.assertEqual(95, cash)

        failing_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 510}]
        executed_order_list, cash = market.execute_order_list(
            failing_buy_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 530}]
        executed_order_list, cash = market.execute_order_list(
            failing_sell_list, datetime(2015, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_order_list_not_exist = [{
            'symbol': 'TWTR',
            'action': Action.buy,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            failing_order_list_not_exist, datetime(2013, 1, 5), Period.day)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

    def test_stooq_quote_source_hour(self):
        market = Market(StooqQuoteSource(), self._order_cost)
        market.load_data(
            ['GOOG', 'TWTR'],
            datetime(2016, 7, 1),
            datetime(2016, 10, 1))

        success_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 1000}]
        executed_order_list, cash = market.execute_order_list(
            success_buy_list, datetime(2016, 7, 1, 10), Period.hour)
        self.assertEqual(success_buy_list, executed_order_list)
        self.assertEqual(-1005, cash)

        success_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            success_sell_list, datetime(2016, 7, 1, 10), Period.hour)
        self.assertEqual(success_sell_list, executed_order_list)
        self.assertEqual(95, cash)

        failing_buy_list = [{
            'symbol': 'GOOG',
            'action': Action.buy,
            'amount': 1,
            'price': 695}]
        executed_order_list, cash = market.execute_order_list(
            failing_buy_list, datetime(2016, 7, 1, 10), Period.hour)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_sell_list = [{
            'symbol': 'GOOG',
            'action': Action.sell,
            'amount': 1,
            'price': 700}]
        executed_order_list, cash = market.execute_order_list(
            failing_sell_list, datetime(2016, 7, 1, 10), Period.hour)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)

        failing_order_list_not_exist = [{
            'symbol': 'TWTRR',
            'action': Action.buy,
            'amount': 1,
            'price': 100}]
        executed_order_list, cash = market.execute_order_list(
            failing_order_list_not_exist,
            datetime(2013, 7, 1, 10),
            Period.hour)
        self.assertEqual([], executed_order_list)
        self.assertEqual(0, cash)


if __name__ == '__main__':
    unittest.main()
