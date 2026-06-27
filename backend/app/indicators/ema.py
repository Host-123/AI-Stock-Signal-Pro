import pandas as pd


def calculate_ema(close_prices: pd.Series) -> dict:
    """
    Calculate EMA20, EMA50 and EMA200.

    Returns:
        {
            "ema20": float,
            "ema50": float,
            "ema200": float
        }
    """

    ema20 = close_prices.ewm(span=20, adjust=False).mean().iloc[-1]
    ema50 = close_prices.ewm(span=50, adjust=False).mean().iloc[-1]
    ema200 = close_prices.ewm(span=200, adjust=False).mean().iloc[-1]

    return {
        "ema20": round(float(ema20), 2),
        "ema50": round(float(ema50), 2),
        "ema200": round(float(ema200), 2),
    }