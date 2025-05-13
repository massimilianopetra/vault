from data_fetcher import get_hourly_prices, simulate_volume_heatmap
from forecaster import calculate_forecast_range, save_suggested_range
from notifier import send_alert
from config import CURRENT_RANGE, RANGE_CONFIDENCE, FORECAST_HOURS
from utils import ensure_output_dir

def main():
    ensure_output_dir()
    prices = get_hourly_prices()
    lower, upper, current_price = calculate_forecast_range(prices, RANGE_CONFIDENCE, FORECAST_HOURS)
    
    print(f"\n📈 Prezzo attuale: {current_price:.2f} USD")
    print(f"📊 Range previsto: [{lower:.2f}, {upper:.2f}] (confidenza {int(RANGE_CONFIDENCE*100)}%)")
    print(f"📘 Range attuale: {CURRENT_RANGE}")

    if current_price < CURRENT_RANGE[0] or current_price > CURRENT_RANGE[1]:
        msg = f"⚠️ Prezzo fuori dal range attuale! Considera la riallocazione.\nNuovo range suggerito: [{lower:.2f}, {upper:.2f}]"
        send_alert(msg)
    else:
        print("✅ Nessuna riallocazione necessaria.")

    save_suggested_range(lower, upper, current_price)

    # Heatmap volume (opzionale)
    print("\n🔍 Heatmap volume (score 0-1):")
    heatmap_df = simulate_volume_heatmap(prices)
    print(heatmap_df.tail(5))

if __name__ == "__main__":
    main()
