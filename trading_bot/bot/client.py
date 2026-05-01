import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger("client")

TESTNET_BASE_URL = "https://testnet.binancefuture.com"

def get_client() -> Client:
    """Initialize and return Binance Futures Testnet client."""

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing API credentials. Check your .env file.")
        raise EnvironmentError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env")

    try:
        client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True
        )
        client.FUTURES_URL = TESTNET_BASE_URL + "/fapi"
        logger.info("Binance Futures Testnet client initialized successfully.")
        return client

    except BinanceAPIException as e:
        logger.error(f"Binance API error during client init: {e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during client init: {str(e)}")
        raise