import requests
import pandas as pd
from config import ASSET, CURRENCY

def get_hourly_prices():
    url = f"https://api.coingecko.com/api/v3/coins/{ASSET}/market_chart"
    params = {
        'vs_currency': CURRENCY,
        'days': 2,
        'interval': 'hourly'
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def simulate_volume_heatmap(prices_df):
    # Semplice simulazione di volume: variazione assoluta oraria
    prices_df['delta'] = prices_df['price'].diff().abs()
    prices_df['volume_score'] = prices_df['delta'] / prices_df['delta'].max()
    return prices_df[['timestamp', 'price', 'volume_score']]
