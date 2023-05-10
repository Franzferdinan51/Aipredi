from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def predict():
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
        'kucoin_price': kucoin_price,
        'lr_rmse': lr_rmse,
        'lr_r2': lr_r2,
        'rf_rmse': rf_rmse,
        'rf_r2': rf_r2
    }

    # Return response as JSON
    return jsonify(response)
