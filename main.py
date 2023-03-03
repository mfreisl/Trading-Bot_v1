import requests as rq
import alpaca_trade_api as api
import yfinance as yf
import pandas_ta as ta

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from params import TAKE_PROFIT_DELTA, TELEGRAM_BOT_ID, TELEGRAM_CHAT_ID, TELEGRAM_URL, \
    TRADER_BOT_NAME, SCREENER_NASDAQ_COUNT, SCREENER_INTERVAL, SCREENER_PERIOD, \
    TRADER_API_KEY, TRADER_API_SECRET, TRADER_API_URL, TRADER_API, \
    trading_client

from screen_stocks import ScreenStocks
from check_stocks import CheckStock
from telegram import send_message


# Documentation: https://alpaca.markets/docs/trading/getting_started/


#Get predictions from LSTM neural network
def Predict(stock):
  predictions = [100.24, 155.33, 140.55]

  # Here we have to organize communication between our algorithm and LSTM Model \
  # to get predictions by ticker for the particular stock.
  # But this is the question to the infrastructure.
  # I am gonna consider it in the next article "Infrastructure itself".

  return predictions

############ Execute Trades ############
def Trade(api, stock, operation, shares_to_trade, take_profit, stop_loss):
  api.submit_order(symbol = stock, qty = shares_to_trade, side = operation, type = 'market',
                  order_class = 'bracket', time_in_force = 'day',
                  take_profit = {'limit_price': take_profit},
                  stop_loss = {'stop_price': stop_loss})
  message = f'\n\t*{stock}*, qty _{shares_to_trade}_ \n\t\twere {operation}'
  send_message(f'{TRADER_BOT_NAME}: we entered the market with:' + message)
  return True

############ MAIN script ############
def trading_bot_main():
    trader_api = api.REST(TRADER_API_KEY, TRADER_API_SECRET, TRADER_API_URL)
    account = trader_api.get_account()
    clock = trader_api.get_clock()

    if bool(account) == True:
        message = f'''{TRADER_BOT_NAME}: for *{account.account_number}*
        current capital is _{account.portfolio_value}$_
        and non marginable buying power is _{account.non_marginable_buying_power}$_'''
        send_message(message)

    if clock.is_open == True:
        if float(account.non_marginable_buying_power) < CASH_LIMIT:
            message = f"{TRADER_BOT_NAME}: there is no cash on the account or limit reached!"
            send_message(message)
        else:
            # Screen stocks
            screened = ScreenStocks(trader_api)
            # Check limit and trade
            if len(screened) > 0:
                CASH_FOR_TRADE_PER_SHARE = (float(account.non_marginable_buying_power) - CASH_LIMIT) / len(screened)
                for item in screened:
                    predictions = Predict(item['stock'])
                    STOCK = item['stock']
                    OPERATION = 'buy' if item['direction'] == 'UP' else 'sell'
                    STOP_LOSS = min([item['stop_loss']] + predictions) if item['direction'] == 'UP' else max([item['stop_loss']] + predictions)
                    TAKE_PROFIT = max([item['take_profit']] + predictions) if item['direction'] == 'UP' else min([item['take_profit']] + predictions)
                    SHARE_PRICE = round(min(STOP_LOSS, TAKE_PROFIT), 2)
                    SHARES_TO_TRADE = int(CASH_FOR_TRADE_PER_SHARE / SHARE_PRICE)
                    try:
                        if abs(STOP_LOSS - TAKE_PROFIT) > SHARE_PRICE * TAKE_PROFIT_DELTA and SHARES_TO_TRADE > 0:
                            Trade(api, STOCK, OPERATION, SHARES_TO_TRADE, TAKE_PROFIT, STOP_LOSS)
                            print(f'\n{STOCK}: {STOP_LOSS}, {TAKE_PROFIT}, {OPERATION}, {SHARES_TO_TRADE}')
                    except:
                        pass


    portfolio = trader_api.list_positions()
    if bool(portfolio) == True:
        message = f'{TRADER_BOT_NAME}: we have {len(portfolio)} opened positions.'
        for i in portfolio:
            message = message + f'\n\t*{i.symbol}*: qty {i.qty} {i.side} for _{i.market_value}$_ \n\t\t\tcurrent price _{i.current_price}$_ \n\t\t\tprofit _{i.unrealized_pl}$_'
        send_message(message)

    if clock.is_open == False:
        message = f"{TRADER_BOT_NAME}: the market is *CLOSED*, let's try later on!"
        send_message(message)

    return f'{TRADER_BOT_NAME}: DONE!'

positions = trading_client.get_all_positions()
for position in positions:
    for property_name, value in position:
        print(f"\"{property_name}\": {value}")


if __name__ == '__main__':
    trading_bot_main()
