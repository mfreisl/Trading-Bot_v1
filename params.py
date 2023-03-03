import os
import numpy as np
import alpaca_trade_api as api
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

##################   SETTINGS   ##################
TRADER_BOT_NAME = 'Mathias Trading Bot'

TRADER_API_KEY= os.environ.get("TRADER_API_KEY")
TRADER_API_SECRET = os.environ.get("TRADER_API_SECRET")
TRADER_API_URL = os.environ.get("TRADER_API_URL")
TRADER_API = api.REST(TRADER_API_KEY, TRADER_API_SECRET, TRADER_API_URL)
trading_client = TradingClient(TRADER_API_KEY, TRADER_API_SECRET, paper=True)


TELEGRAM_URL = os.environ.get("TELEGRAM_URL")
TELEGRAM_BOT_ID = os.environ.get("TELEGRAM_BOT_ID")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SCREENER_INTERVAL = '5m'
SCREENER_PERIOD = '1d'
SCREENER_NASDAQ_COUNT = 100

TAKE_PROFIT_DELTA = 0.05
CASH_LIMIT = 10000
