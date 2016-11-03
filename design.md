# Design

## Data Structure

* Period enum: {day, hour, minute}
* Action enum: {buy, sell}
* Quote: {symbol, datetime, high, low, volumn, period}
* Order: {symbol, action, amount, price}
* News: {symbol, list({datetime, title, text})}

## Class

### Market
* __init__(QuoteSource, order_cost): Market construction method
* execute_order_list(order_list, datetime, period):
  returns (executed_order_list, cash). If action is sell, cash is positive,
  otherwise negative. cash includes broker fees as well
* load_data(symbol_list, start_datetime, end_datetime):
  loads market data of a list of symbols from start_datetime to end_datetime.
* get_quote_map(datetime, period): returns map<symbol, Quote>
* get_datetime_list(period) virtual: get a list of market opening periods

### QuoteSource
* load_data(symbol_list, start_datetime, end_datetime) virtual:
  loads market data of a list of symbols from start_datetime to end_datetime.
* get_quote_map(datetime, period) virtual: map<symbol, Quote>
* get_datetime_list(period) virtual: get a list of market opening periods

#### Implementation
* YahooQuoteSource: Loads data from Yahoo (daily).
* GoogleQuoteSource: Loads data from Google (daily).
* StooqQuoteSource: Loads data from Stooq (daily, hourly, minute).

### NewsSource
* load_data(symbol_list, start_datetime, end_datetime) virtual:
  loads market news of a list of symbols from start_datetime to end_datetime.
* get_news(start_datetime, end_datetime) virtual: returns a list of News

#### Implementation
* GoogleNewsSource: Loads data from Google.
