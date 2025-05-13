import requests
from config import USE_TELEGRAM, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_alert(message):
    print(f"[ALERT] {message}")
    if USE_TELEGRAM:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            print(f"Errore invio Telegram: {e}")
