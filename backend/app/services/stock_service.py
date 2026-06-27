import yfinance as yf

from app.core.logger import logger
from app.indicators.ema import calculate_ema
from app.indicators.rsi import calculate_rsi


def get_stock_price(symbol: str):
    """
    Fetch stock data and calculate technical indicators.
    """

    try:

        logger.info(f"Fetching market data: {symbol}")

        stock = yf.Ticker(symbol)
        history = stock.history(period="6mo")

        if history.empty:
            return {
                "success": False,
                "message": "Stock not found",
                "data": None,
            }

        latest = history.iloc[-1]

        open_price = float(latest["Open"])
        high_price = float(latest["High"])
        low_price = float(latest["Low"])
        close_price = float(latest["Close"])
        volume = int(latest["Volume"])

        change = close_price - open_price
        change_percent = (change / open_price) * 100

        # -----------------------------
        # Indicator Engine
        # -----------------------------

        rsi = calculate_rsi(history["Close"])
        ema = calculate_ema(history["Close"])

        # -----------------------------
        # Temporary Signal Logic
        # (Professional Engine আসবে Phase 5-এ)
        # -----------------------------

        signal = "HOLD"

        if rsi < 30:
            signal = "BUY"

        elif rsi > 70:
            signal = "SELL"

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

        logger.info(f"{symbol} analysis completed.")

        return {
            "success": True,
            "message": "Stock fetched successfully",
            "data": {
                "symbol": symbol,
                "price": round(close_price, 2),
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "volume": volume,
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),

                "rsi": rsi,

                "ema20": ema["ema20"],
                "ema50": ema["ema50"],
                "ema200": ema["ema200"],

                "signal": signal,

                "entry": entry,
                "stop_loss": stop_loss,
                "target1": target1,
                "target2": target2,
                "exit": exit_price,
            },
        }

    except Exception as e:

        logger.exception(e)

        return {
            "success": False,
            "message": str(e),
            "data": None,
        }


def get_watchlist():

    watchlist = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
    ]

    result = []

    for symbol in watchlist:
        result.append(get_stock_price(symbol))

    return {
        "success": True,
        "message": "Watchlist fetched successfully",
        "data": result,
    }