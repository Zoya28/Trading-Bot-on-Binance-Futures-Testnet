"""Input validation logic — kept separate so CLI stays clean."""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """Symbol must be a non-empty uppercase string like BTCUSDT."""
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be one of {VALID_SIDES}. Got: '{side}'")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}. Got: '{order_type}'")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(f"Quantity must be a number. Got: '{quantity}'")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {qty}")
    return qty


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Price must be a number. Got: '{price}'")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0. Got: {p}")
    return p


def validate_all(symbol, side, order_type, quantity, price=None):
    """
    Run all validations and return cleaned values.
    Raises ValueError with a clear message on any failure.
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        price = validate_price(str(price))

    return symbol, side, order_type, quantity, price