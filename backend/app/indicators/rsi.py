from ta.momentum import RSIIndicator


def calculate_rsi(close_prices, window: int = 14) -> float:
    """
    Calculate the latest RSI value.

    Args:
        close_prices: Pandas Series containing closing prices.
        window: RSI period (default = 14)

    Returns:
        Latest RSI value rounded to 2 decimal places.
    """

    rsi_series = RSIIndicator(
        close=close_prices,
        window=window,
    ).rsi()

    latest_rsi = float(rsi_series.iloc[-1])

    return round(latest_rsi, 2)