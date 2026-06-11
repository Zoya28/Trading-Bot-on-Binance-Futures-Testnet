# Binance Futures Testnet Trading Bot

A simple Python CLI trading bot for Binance Futures Testnet (USDT-M).

---

## Setup

### 1. Get Testnet API Keys
1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in and **"Generate API Key"**
3. Copy your **API Key** and **Secret Key**

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

**Windows (CMD):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_secret_key_here
```

---

## How to Run

Run all commands from the `trading_bot/` folder.

## Streamlit UI

Run:

```bash
streamlit run app.py
---

## CLI

### Place a MARKET order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000
```

### Help
```bash
python cli.py --help
```

---

## Example Output

```
────────────────────────────────────────
  ORDER REQUEST SUMMARY
────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
────────────────────────────────────────

────────────────────────────────────────
  ORDER RESPONSE
────────────────────────────────────────
  Order ID     : 123456789
  Symbol       : BTCUSDT
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 43250.50
  Type         : MARKET
  Side         : BUY
────────────────────────────────────────

✅ Order placed successfully!
```

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py        # Binance API calls + signing
│   ├── orders.py        # Order placement logic
│   ├── validators.py    # Input validation
│   └── logging_config.py
├── cli.py               # CLI entry point (argparse)
├── requirements.txt
└── README.md
```

---

## Logs

Logs are saved to `logs/trading_bot.log` automatically.
- Console shows INFO and above
- Log file captures DEBUG (full request/response details)

---

## Assumptions

- Only USDT-M Futures Testnet is supported
- Credentials are passed via environment variables (not hardcoded)
- `timeInForce` is set to `GTC` (Good Till Cancel) for all LIMIT orders