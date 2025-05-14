# charts.py
import io
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import EXCHANGERATE_API_URL, COINGECKO_API_URL
from utils import CRYPTO_IDS

def generate_chart(from_curr, to_curr):
    from_id = CRYPTO_IDS.get(from_curr)
    to_id = CRYPTO_IDS.get(to_curr)
    dates = []
    values = []
    title = f"{from_curr} to {to_curr} - 7 days"
    if not from_id and not to_id:
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=6)
        url = (f"{EXCHANGERATE_API_URL}/timeseries?"
               f"start_date={start_date}&end_date={end_date}"
               f"&base={from_curr}&symbols={to_curr}")
        try:
            data = requests.get(url).json()
            rates = data.get("rates", {})
            for date_str in sorted(rates.keys()):
                rate = rates[date_str].get(to_curr)
                if rate is not None:
                    dates.append(datetime.fromisoformat(date_str))
                    values.append(rate)
        except Exception:
            return None
    else:
        if from_id:
            coin_id = from_id
            vs_currency = to_curr.lower()
        else:
            coin_id = to_id
            vs_currency = from_curr.lower()
        url = (f"{COINGECKO_API_URL}/coins/{coin_id}/market_chart?"
               f"vs_currency={vs_currency}&days=7")
        try:
            data = requests.get(url).json()
            prices = data.get("prices", [])
            for ts, price in prices:
                dates.append(datetime.fromtimestamp(ts/1000))
                values.append(price)
        except Exception:
            return None
    if not dates or not values:
        return None
    plt.figure(figsize=(6, 4))
    plt.plot(dates, values, marker="o")
    plt.title(title)
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf
