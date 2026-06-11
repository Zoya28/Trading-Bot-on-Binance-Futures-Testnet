"""
CLI entry point using argparse.
Usage examples in README.md
"""

import argparse
import sys
from bot.orders import submit_order
from bot.logging_config import setup_logger

logger = setup_logger()


def print_response(response: dict):
    """Pretty-print the order response from Binance."""
    print("\n" + "─" * 40)
    print("  ORDER RESPONSE")
    print("─" * 40)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price    : {response.get('avgPrice', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print("─" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity",   required=True,  help="Amount to trade, e.g. 0.01")
    parser.add_argument("--price",      required=False, help="Required for LIMIT orders, e.g. 30000")

    args = parser.parse_args()

    try:
        response = submit_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price
        )
        print_response(response)
        print("\nOrder placed successfully!\n")
        logger.info(f"Order SUCCESS | orderId={response.get('orderId')} | status={response.get('status')}")

    except ValueError as e:
        print(f"\nValidation Error: {e}\n")
        logger.warning(f"Validation error: {e}")
        sys.exit(1)

    except RuntimeError as e:
        print(f"\nAPI/Network Error: {e}\n")
        logger.error(f"Runtime error: {e}")
        sys.exit(1)

    except EnvironmentError as e:
        print(f"\nConfiguration Error: {e}\n")
        logger.error(f"Environment error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()