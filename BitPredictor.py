from flask import Flask, jsonify
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
    'X-CMC_PRO_API_KEY': 'YOUR_API_KEY'
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

 # Machine learning models
x = [[coin['pct_change_21d'], coin['pct_change_180d'], coin['pct_change_365d']] for coin in coins]
y = [1 if coin['symbol'] == 'BTC' else 0 for coin in coins]

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train linear regression model
lr_model = linear_regression_model(x_train, y_train)

# Train random forest regression model
rf_model = random_forest_model(x_train, y_train)

# Make predictions
lr_predictions = lr_model.predict(x_test)
rf_predictions = rf_model.predict(x_test)

# Evaluate models
lr_rmse = mean_squared_error(y_test, lr_predictions, squared=False)
lr_r2 = r2_score(y_test, lr_predictions)
rf_rmse = mean_squared_error(y_test, rf_predictions, squared=False)
rf_r2 = r2_score(y_test, rf_predictions)

# Plot predictions
fig, ax = plt.subplots()
ax.scatter(y_test, lr_predictions, label=f'Linear Regression\nRMSE: {lr_rmse:.2f}, R2: {lr_r2:.2f}')
ax.scatter(y_test, rf_predictions, label=f'Random Forest\nRMSE: {rf_rmse:.2f}, R2: {rf_r2:.2f}')
ax.set_xlabel('True values')
ax.set_ylabel('Predicted values')
ax.set_title('Bitcoin price prediction')
ax.legend()

# Save plot to file
plt.savefig('bitcoin_price_prediction.png')

# Prepare response
response = {
    'binance_price': binance_price,
    'kucoin_price': kucoin_price
}

return jsonify(response)
