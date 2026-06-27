import yfinance as yf
from ta.momentum import RSIIndicator


def get_stock_price(symbol: str):
    stock = yf.Ticker(symbol)

    # 6 মাসের ডেটা RSI হিসাবের জন্য
    info = stock.history(period="6mo")

    if info.empty:
        return {"error": "Stock not found"}

    # RSI Calculation
    rsi_indicator = RSIIndicator(close=info["Close"], window=14)
    info["RSI"] = rsi_indicator.rsi()

    latest = info.iloc[-1]

    open_price = float(latest["Open"])
    high_price = float(latest["High"])
    low_price = float(latest["Low"])
    close_price = float(latest["Close"])
    volume = int(latest["Volume"])

    change = close_price - open_price
    change_percent = (change / open_price) * 100

    rsi = round(float(latest["RSI"]), 2)

    # Basic Signal Logic (শুধু RSI ভিত্তিক - আপাতত)
    signal = "HOLD"

    if rsi < 30:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"

    # Entry / Exit / Target / Stop Loss
    entry = "-"
    stop_loss = "-"
    target1 = "-"
    target2 = "-"
    exit_price = "-"

    if signal == "BUY":
        entry = round(close_price, 2)
        stop_loss = round(low_price, 2)
        target1 = round(close_price * 1.02, 2)
        target2 = round(close_price * 1.04, 2)

    elif signal == "SELL":
        exit_price = round(close_price, 2)

    return {
        "symbol": symbol,
        "price": round(close_price, 2),
        "open": round(open_price, 2),
        "high": round(high_price, 2),
        "low": round(low_price, 2),
        "volume": volume,
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
        "rsi": rsi,
        "signal": signal,
        "entry": entry,
        "stop_loss": stop_loss,
        "target1": target1,
        "target2": target2,
        "exit": exit_price
    }


def get_watchlist():

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS"
    ]

    result = []

    for symbol in stocks:
        result.append(get_stock_price(symbol))

    return result