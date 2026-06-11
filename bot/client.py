"""
Binance Futures Testnet API client.
Handles authentication, signing, and raw HTTP calls.
"""

import hashlib
import hmac
import time
import os
import requests
from bot.logging_config import setup_logger
from dotenv import load_dotenv

load_dotenv()

logger = setup_logger()

BASE_URL = "https://testnet.binancefuture.com"


def _sign(params: dict, secret: str) -> str:
    """Create HMAC-SHA256 signature required by Binance API."""
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()


def get_credentials():
    """Read API key and secret from environment variables."""
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        raise EnvironmentError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set as environment variables."
        )
    return api_key, api_secret

def get_current_price(symbol: str) -> float:
    """Fetch current market price for a symbol."""
    
    response = requests.get(
        f"{BASE_URL}/fapi/v1/ticker/price",
        params={"symbol": symbol},
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return float(data["price"])

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Send a POST /fapi/v1/order request to Binance Futures Testnet.
    Returns the parsed JSON response.
    """
    api_key, api_secret = get_credentials()
    
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  

    params["signature"] = _sign(params, api_secret)

    headers = {"X-MBX-APIKEY": api_key}

    logger.debug(f"API Request -> POST /fapi/v1/order | Params: { {k: v for k, v in params.items() if k != 'signature'} }")

    try:
        response = requests.post(
            f"{BASE_URL}/fapi/v1/order",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logger.debug(f"API Response -> {data}")
        return data

    except requests.exceptions.HTTPError as e:
        error_msg = e.response.json().get("msg", str(e))
        raise RuntimeError(f"Binance API Error: {error_msg}")

    except requests.exceptions.ConnectionError:
        logger.error("Network error: Could not connect to Binance Testnet.")
        raise RuntimeError("Network error: Could not connect to Binance Testnet. Check your internet.")

    except requests.exceptions.Timeout:
        logger.error("Request timed out.")
        raise RuntimeError("Request timed out. Try again.")