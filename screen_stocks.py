import requests as rq
import alpaca_trade_api as api
import yfinance as yf
import pandas_ta as ta

from params import TAKE_PROFIT_DELTA, TELEGRAM_BOT_ID, TELEGRAM_CHAT_ID, TELEGRAM_URL, \
    TRADER_BOT_NAME, SCREENER_NASDAQ_COUNT, SCREENER_INTERVAL, SCREENER_PERIOD, \
        TRADER_API_KEY, TRADER_API_SECRET, TRADER_API_URL, TRADER_API

from check_stocks import CheckStock

def ScreenStocks(trader_api):
    assets = trader_api.list_assets(status='active', asset_class='us_equity')
    assets = [x for x in assets if x.shortable == True and x.exchange == 'NASDAQ']
    stocks = [x.symbol for x in assets][:SCREENER_NASDAQ_COUNT]

    screened = []
    for st in stocks:
        # Here we are calling the CheckStock function from earlier for all stocks in the list
        _stock = CheckStock(st)
        if _stock != {}:
            screened.append(_stock)
    screened = [x for x in screened if abs(x['stop_loss'] - x['take_profit']) > min(x['stop_loss'], x['take_profit']) * TAKE_PROFIT_DELTA]
    # returns an already screened list of stocks, according to the set parameters
    return screened
