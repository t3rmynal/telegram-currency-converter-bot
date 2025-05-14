# utils.py
import requests
from config import EXCHANGERATE_API_URL, COINGECKO_API_URL

user_data = {}

CRYPTO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "TON": "toncoin",
    "USDT": "tether"
}

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"language": None, "favorites": []}
    return user_data[user_id]

def parse_conversion(text):
    parts = text.strip().split()
    if len(parts) == 4 and parts[2].lower() == "to":
        try:
            amount = float(parts[0])
            from_curr = parts[1].upper()
            to_curr = parts[3].upper()
            return amount, from_curr, to_curr
        except ValueError:
            return None
    return None

def convert_fiat(amount, from_curr, to_curr):
    url = f"{EXCHANGERATE_API_URL}/convert?from={from_curr}&to={to_curr}&amount={amount}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        result = data.get("result", None)
        return result
    except Exception:
        return None

def convert_crypto(amount, from_curr, to_curr):
    from_id = CRYPTO_IDS.get(from_curr)
    to_id = CRYPTO_IDS.get(to_curr)
    # Crypto to Crypto or Crypto to Fiat
    if from_id:
        url = f"{COINGECKO_API_URL}/simple/price?ids={from_id}&vs_currencies={to_curr.lower()}"
        try:
            data = requests.get(url, timeout=10).json()
            price = data.get(from_id, {}).get(to_curr.lower())
            if price is None:
                return None
            return price * amount
        except Exception:
            return None
    # Fiat to Crypto
    if to_id:
        url = f"{COINGECKO_API_URL}/simple/price?ids={to_id}&vs_currencies={from_curr.lower()}"
        try:
            data = requests.get(url, timeout=10).json()
            price = data.get(to_id, {}).get(from_curr.lower())
            if price is None or price == 0:
                return None
            return amount / price
        except Exception:
            return None
    return None

def convert_custom(amount, from_curr, to_curr):
    # Example static rates for FPI Bank
    rate = None
    if from_curr == "FPI":
        if to_curr == "USD":
            rate = 150
        elif to_curr == "EUR":
            rate = 130
    elif to_curr == "FPI":
        if from_curr == "USD":
            rate = 1/150
        elif from_curr == "EUR":
            rate = 1/130
    if rate is None:
        return None
    return amount * rate
