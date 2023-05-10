from flask import Flask, jsonify
from PriceUpdater import update_prices
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# CoinMarketCap API
cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
cmc_params = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}
cmc_headers = {
    'X-CMC_PRO_API_KEY': 'c4f907a0-7d22-4058-8ef8-b2676295afe3'
}

# Binance API
binance_url = 'https://api.binance.com/api/v3/ticker/24hr'
binance_params = {
    'symbol': 'BTCUSDT'
}

# Kucoin API
kucoin_url = 'https://api.kucoin.com/api/v1/market/candles'
kucoin_params = {
    'symbol': 'BTC-USDT',
    'startAt': (datetime.now() - timedelta(days=365)).timestamp() * 1000,
    'endAt': datetime.now().timestamp() * 1000,
    'type': '1day'
}

# Linear Regression model
def linear_regression_model(x_train, y_train):
    lr_model = LinearRegression()
    lr_model.fit(x_train, y_train)
    return lr_model

# Random Forest Regression model
def random_forest_model(x_train, y_train):
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(x_train, y_train)
    return rf_model

@app.route('/')
def index():
    return 'Welcome to the crypto prediction app!'

@app.route('/predict')
def predict():
    # Get data from APIs
    cmc_response = requests.get(cmc_url, params=cmc_params, headers=cmc_headers).json()
    binance_response = requests.get(binance_url, params=binance_params).json()
    kucoin_response = requests.get(kucoin_url, params=kucoin_params).json()

    # Process data
    cmc_data = cmc_response['data']
    binance_price = float(binance_response['lastPrice'])
    kucoin_data = pd.DataFrame(kucoin_response['data'], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    kucoin_price = float(kucoin_data['close'].iloc[-1])

    coins = []
    for coin in cmc_data:
        symbol = coin['symbol']
        quote = coin['quote']['USD']
        pct_change_7d = quote['percent_change_7d']
        pct_change_21d = quote['percent_change_21d']
        pct_change_180d = quote['percent_change_180d']
        pct_change_365d = quote['percent_change_365d']

        coins.append({
            'symbol': symbol,
            'pct_change_7d': pct_change_7d,
            'pct_change_21d': pct_change_21d,
            'pct_change_180d': pct_change_180d,
            'pct_change_365d': pct_change_365d
        })

    coins = sorted(coins, key=lambda x: x['pct_change_7d'], reverse=True)[:10]

