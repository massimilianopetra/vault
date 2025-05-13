import numpy as np
from scipy.stats import norm
import json
from config import RANGE_CONFIDENCE, FORECAST_HOURS

def calculate_forecast_range(prices, confidence, forecast_hours):
    log_returns = np.log(prices['price'] / prices['price'].shift(1)).dropna()
    mu = log_returns.mean()
    sigma = log_returns.std()
    Z = norm.ppf([(1 - confidence) / 2, 1 - (1 - confidence) / 2])
    P0 = prices['price'].iloc[-1]
    dt = forecast_hours / 24
    lower = P0 * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[0])
    upper = P0 * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[1])
    return lower, upper, P0

def save_suggested_range(lower, upper, current_price):
    result = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "price_now": round(current_price, 4),
        "suggested_range": [round(lower, 2), round(upper, 2)]
    }
    with open("output/suggested_range.json", "w") as f:
        json.dump(result, f, indent=4)
