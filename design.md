# Design

## Data Structure

* Period enum: {day, hour, minute}
* Quote: {symbol, datetime, high, low, volumn, period}
* Order: list({symbol, amount, price})
* News: {symbol, datetime, list({title, text)}

## Class

### Market
* execute_order(order, datetime, period): returns {executed order, cost}.
  cost contains broker fees.
* load_data(QuoteSource, symbol_list, start_datetime, end_datetime) virtual:
  loads market data of a list of symbols from start_datetime to end_datetime.
* get_quote virtual(datetime, period): returns a list of Quotes

### QuoteSource
* load_data(symbol_list, start_datetime, end_datetime) virtual:
  loads market data of a list of symbols from start_datetime to end_datetime.
* get_quote(datetime, period) virtual: returns a list of Quotes

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
