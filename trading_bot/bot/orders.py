from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import setup_logger

logger = setup_logger("orders")

def set_leverage(client: Client, symbol: str, leverage: int) -> dict:
    """Set leverage for a symbol on Binance Futures Testnet."""

    logger.info(f"Setting leverage | symbol={symbol} leverage={leverage}x")

    try:
        response = client.futures_change_leverage(
            symbol=symbol,
            leverage=leverage
        )
        logger.debug(f"Leverage response: {response}")
        logger.info(f"Leverage set to {leverage}x for {symbol}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API error (set_leverage): code={e.status_code} msg={e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error (set_leverage): {str(e)}")
        raise
def place_market_order(client: Client, symbol: str, side: str, quantity: float) -> dict:
    """Place a MARKET order on Binance Futures Testnet."""

    logger.info(f"Placing MARKET order | symbol={symbol} side={side} qty={quantity}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logger.debug(f"MARKET order raw response: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API error (MARKET): code={e.status_code} msg={e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error (MARKET order): {str(e)}")
        raise


def place_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float) -> dict:
    """Place a LIMIT order on Binance Futures Testnet."""

    logger.info(f"Placing LIMIT order | symbol={symbol} side={side} qty={quantity} price={price}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"   # Good Till Cancelled
        )
        logger.debug(f"LIMIT order raw response: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API error (LIMIT): code={e.status_code} msg={e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error (LIMIT order): {str(e)}")
        raise


def place_stop_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> dict:
    """Place a STOP-LIMIT order on Binance Futures Testnet (Bonus)."""

    logger.info(f"Placing STOP-LIMIT order | symbol={symbol} side={side} qty={quantity} price={price} stopPrice={stop_price}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            timeInForce="GTC"
        )
        logger.debug(f"STOP-LIMIT order raw response: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API error (STOP-LIMIT): code={e.status_code} msg={e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error (STOP-LIMIT order): {str(e)}")
        raise


def parse_order_response(response: dict) -> dict:
    """Extract the key fields from an order response."""

    return {
        "orderId":     response.get("orderId"),
        "symbol":      response.get("symbol"),
        "side":        response.get("side"),
        "type":        response.get("type"),
        "status":      response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice":    response.get("avgPrice"),
        "price":       response.get("price"),
        "origQty":     response.get("origQty"),
        "timeInForce": response.get("timeInForce"),
    }