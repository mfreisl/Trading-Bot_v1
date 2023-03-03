import requests as rq
import alpaca_trade_api as api
import yfinance as yf
import pandas_ta as ta

from params import TAKE_PROFIT_DELTA, TELEGRAM_BOT_ID, TELEGRAM_CHAT_ID, TELEGRAM_URL, \
    TRADER_BOT_NAME, SCREENER_NASDAQ_COUNT, SCREENER_INTERVAL, SCREENER_PERIOD, \
        TRADER_API_KEY, TRADER_API_SECRET, TRADER_API_URL, TRADER_API

def CheckStock(stock):
    data = {}
    try:
        df = yf.download(stock, period = SCREENER_PERIOD, interval = SCREENER_INTERVAL)
        if (len(df) > 0):
            df['RSI'] = ta.rsi(df['Close'], timeperiod=14)
            #In our case, to identify this pattern we use Bollinger Bands with period = 20 and non-standard deviation equals to 2.3.
            #This number is important, believe me. I got this setup for BBANDS based on my own experiments.
            #They work much better than the standard deviation equaling 2.
            #Actually these numbers are so important that most investment firms protect them in their public relations and non-disclosure agreements.
            bbands = ta.bbands(df['Close'], length = 20, std=2.3)
            df['L'] = bbands['BBL_20_2.3']
            df['M'] = bbands['BBM_20_2.3']
            df['U'] = bbands['BBU_20_2.3']

            previous2_bar = df[-3:].head(1)
            previous_bar = df[-2:].head(1)
            current_bar = df[-1:]

            if current_bar['RSI'].values[0] > 70 and \
                current_bar['Close'].values[0] > current_bar['U'].values[0]:
                    data = { 'direction': 'DOWN', 'stock' : stock, 'stop_loss': round(max(previous_bar['High'].values[0], previous2_bar['High'].values[0], previous_bar['U'].values[0]), 2), \
                            'take_profit': round(min(previous_bar['Low'].values[0], previous2_bar['Low'].values[0], previous_bar['M'].values[0]), 2) }
            elif current_bar['RSI'].values[0] < 30 and \
                current_bar['Close'].values[0] < current_bar['L'].values[0]:
                    data = { 'direction': 'UP', 'stock' : stock, 'stop_loss': round(min(previous_bar['Low'].values[0], previous2_bar['Low'].values[0], previous_bar['L'].values[0]), 2), \
                            'take_profit': round(max(previous_bar['High'].values[0], previous2_bar['High'].values[0], previous_bar['M'].values[0]), 2) }
    except:
        pass

    return data
