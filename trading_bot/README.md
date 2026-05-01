# 🤖 Binance Futures Testnet Trading Bot

A Python CLI trading bot that places orders on Binance Futures Testnet (USDT-M).
Built with clean separation of concerns: API client, order logic, validation, and CLI layers.

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py        # Package marker (empty)
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement + leverage logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # Auto-generated log files
├── .env                   # API keys (never committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Steps

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/binance-futures-trading-bot.git
cd binance-futures-trading-bot/trading_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Binance Futures Testnet API Keys
- Go to: https://testnet.binancefuture.com
- Log in with GitHub
- Generate API Key + Secret

### 4. Create your `.env` file
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

> ⚠️ Never commit your `.env` file — it is already listed in `.gitignore`

---

## 🚀 How to Run

> All commands must be run from inside the `trading_bot/` directory.

### ✅ Place a MARKET order
```bash
# BUY 0.001 BTC at market price with default 10x leverage
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# BUY 0.001 BTC at market price with 20x leverage
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --leverage 20

# SELL 0.001 BTC at market price
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001 --leverage 10
```

### ✅ Place a LIMIT order
```bash
# BUY 0.001 BTC at $50,000 with 10x leverage
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000

# SELL 0.001 BTC at $100,000 with 15x leverage
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000 --leverage 15
```

### ✅ Place a STOP-LIMIT order (Bonus)
```bash
# SELL 0.001 BTC with stop at $85,000, limit at $84,500, 10x leverage
python cli.py --symbol BTCUSDT --side SELL --type STOP-LIMIT --quantity 0.001 --price 84500 --stop-price 85000 --leverage 10
```

### 📋 View help
```bash
python cli.py --help
```

---

## 🎛️ All CLI Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--symbol` | ✅ Yes | — | Trading pair e.g. `BTCUSDT` |
| `--side` | ✅ Yes | — | `BUY` or `SELL` |
| `--type` | ✅ Yes | — | `MARKET`, `LIMIT`, or `STOP-LIMIT` |
| `--quantity` | ✅ Yes | — | Order quantity e.g. `0.001` |
| `--leverage` | ❌ No | `10` | Leverage 1–125 e.g. `20` |
| `--price` | ⚠️ Conditional | — | Required for `LIMIT` and `STOP-LIMIT` |
| `--stop-price` | ⚠️ Conditional | — | Required for `STOP-LIMIT` only |

---

## 📄 Logging

Logs are saved automatically to:
```
logs/trading_bot_YYYYMMDD.log
```

Each log entry includes:
- Timestamp
- Log level (DEBUG / INFO / WARNING / ERROR)
- Module name (client / orders / validators / cli)
- Full message

Sample log output:
```
2024-01-15 10:23:01 | INFO     | client     | Binance Futures Testnet client initialized successfully.
2024-01-15 10:23:01 | INFO     | orders     | Setting leverage | symbol=BTCUSDT leverage=10x
2024-01-15 10:23:01 | INFO     | orders     | Placing MARKET order | symbol=BTCUSDT side=BUY qty=0.001
2024-01-15 10:23:02 | DEBUG    | orders     | MARKET order raw response: {'orderId': 123456, 'status': 'FILLED', ...}
2024-01-15 10:23:02 | INFO     | cli        | Order placed successfully: {'orderId': 123456, 'status': 'FILLED'}
```

---

## 🛡️ Error Handling

The bot handles:
- ❌ Invalid symbol / side / order type
- ❌ Invalid leverage (must be 1–125)
- ❌ Missing price for LIMIT orders
- ❌ Missing stop price for STOP-LIMIT orders
- ❌ Binance API errors (with error codes)
- ❌ Network failures
- ❌ Missing API credentials in `.env`

---

## 📌 Assumptions

- All orders are placed on **Binance Futures Testnet (USDT-M)**
- Base URL used: `https://testnet.binancefuture.com`
- LIMIT orders use **GTC** (Good Till Cancelled) by default
- Default leverage is **10x** if `--leverage` is not specified
- Leverage is set automatically before every order is placed
- Quantity precision follows Binance testnet rules (e.g., min 0.001 BTC for BTCUSDT)
- Bot always asks for confirmation before placing an order
- Logs are written to `logs/` directory (auto-created if missing)

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| `python-binance` | Binance API wrapper |
| `argparse` | CLI argument parsing (built-in) |
| `rich` | Beautiful terminal output |
| `python-dotenv` | Load `.env` credentials |
| `logging` | Structured log files |

---

## 📝 Bonus Features

- ✅ **STOP-LIMIT orders** supported as a third order type
- ✅ **Leverage selection** via `--leverage` flag (1x–125x, default 10x)
- ✅ **Rich terminal UI** with colored tables for order summary and response
- ✅ **Confirmation prompt** before every order to prevent accidental trades
- ✅ **Structured logging** to both console and log file simultaneously