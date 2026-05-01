from bot.logging_config import setup_logger

logger = setup_logger("validators")

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP-LIMIT"]


def validate_symbol(symbol: str) -> str:
    """Validate and normalize trading symbol."""
    symbol = symbol.strip().upper()
    if not symbol.isalpha() or len(symbol) < 5:
        logger.warning(f"Invalid symbol entered: {symbol}")
        raise ValueError(f"Invalid symbol '{symbol}'. Example: BTCUSDT")
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """Validate order side."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        logger.warning(f"Invalid side entered: {side}")
        raise ValueError(f"Invalid side '{side}'. Must be one of: {VALID_SIDES}")
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        logger.warning(f"Invalid order type entered: {order_type}")
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {VALID_ORDER_TYPES}")
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: str) -> float:
    """Validate quantity is a positive number."""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError()
    except ValueError:
        logger.warning(f"Invalid quantity entered: {quantity}")
        raise ValueError(f"Quantity must be a positive number. Got: '{quantity}'")
    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price: str) -> float:
    """Validate price is a positive number."""
    try:
        p = float(price)
        if p <= 0:
            raise ValueError()
    except ValueError:
        logger.warning(f"Invalid price entered: {price}")
        raise ValueError(f"Price must be a positive number. Got: '{price}'")
    logger.debug(f"Price validated: {p}")
    return p


def validate_all(symbol: str, side: str, order_type: str, quantity: str,
                 price: str = None, stop_price: str = None, leverage: str = "10") -> dict:
    """Run all validations and return cleaned values."""

    result = {
        "symbol":     validate_symbol(symbol),
        "side":       validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity":   validate_quantity(quantity),
        "leverage":   validate_leverage(leverage)
    }

    if order_type.upper() in ["LIMIT", "STOP-LIMIT"]:
        if not price:
            raise ValueError("Price is required for LIMIT and STOP-LIMIT orders.")
        result["price"] = validate_price(price)

    if order_type.upper() == "STOP-LIMIT":
        if not stop_price:
            raise ValueError("Stop price is required for STOP-LIMIT orders.")
        result["stop_price"] = validate_price(stop_price)

    return result
def validate_leverage(leverage: str) -> int:
    """Validate leverage is an integer between 1 and 125."""
    try:
        lev = int(leverage)
        if lev < 1 or lev > 125:
            raise ValueError()
    except ValueError:
        logger.warning(f"Invalid leverage entered: {leverage}")
        raise ValueError(f"Leverage must be an integer between 1 and 125. Got: '{leverage}'")
    logger.debug(f"Leverage validated: {lev}x")
    return lev