from fyers_apiv3 import fyersModel
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

def get_intraday(symbol, interval="1"):
    data = {
        "symbol": f"NSE:{symbol}-EQ",
        "resolution": interval,
        "date_format": "1",
        "range_from": "2025-08-22",   # replace with today’s date
        "range_to": "2025-08-22",
        "cont_flag": "1"
    }
    response = fyers.history(data)
    if "candles" not in response:
        return pd.DataFrame()
    df = pd.DataFrame(response['candles'], columns=["time","open","high","low","close","volume"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    return df

def check_breakout(df, prev_close):
    first_candle = df.between_time("09:15", "09:30")
    if first_candle.empty:
        return None
    high_15 = first_candle["high"].max()
    for idx, row in df.iterrows():
        price = row["close"]
        pct_change = (price - prev_close) / prev_close * 100
        if price > high_15 and 2 <= pct_change <= 3:
            return {"time": idx, "price": price, "pct_change": round(pct_change, 2)}
    return None
