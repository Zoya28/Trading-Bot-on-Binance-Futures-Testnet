"""
Order placement logic.
Sits between the CLI and the raw API client.
"""

from bot.client import place_order
from bot.validators import validate_all
from bot.logging_config import setup_logger

logger = setup_logger()


def submit_order(symbol: str, side: str, order_type: str, quantity: str, price: str = None) -> dict:
    """
    Validate inputs, log the request summary, call the API, and return results.
    Raises ValueError for bad input, RuntimeError for API/network issues.
    """

    # --- Validate ---
    symbol, side, order_type, quantity, price = validate_all(symbol, side, order_type, quantity, price)

    # --- Print + log the request summary ---
    summary_lines = [
        "─" * 40,
        "  ORDER REQUEST SUMMARY",
        "─" * 40,
        f"  Symbol     : {symbol}",
        f"  Side       : {side}",
        f"  Type       : {order_type}",
        f"  Quantity   : {quantity}",
    ]
    if order_type == "LIMIT":
        summary_lines.append(f"  Price      : {price}")
    summary_lines.append("─" * 40)

    print("\n".join(summary_lines))
    logger.info(f"Placing {order_type} {side} order | {symbol} | qty={quantity}" +
                (f" | price={price}" if price else ""))

    # --- Call API ---
    response = place_order(symbol, side, order_type, quantity, price)

    return response