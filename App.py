import streamlit as st
import pandas as pd
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime as dt
import os

st.title("📈 Nifty 500 Screener")
st.write("Live screener for stocks moving 2-3% and crossing first 15m candle high.")

# 🔑 Read secrets (set in Streamlit Cloud later)
client_id = st.secrets["client_id"]
secret_key = st.secrets["secret_key"]
redirect_uri = st.secrets["redirect_uri"]
access_token = st.secrets["access_token"]

# ✅ Initialize Fyers
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

# 🕒 Function to fetch intraday candles
def get_intraday(symbol="NSE:RELIANCE-EQ", interval="1", start=None, end=None):
    data = {
        "symbol": symbol,
        "resolution": interval,
        "date_format": "1",
        "range_from": start,
        "range_to": end,
        "cont_flag": "1"
    }
    return fyers.history(data)

# 🎯 Screener logic (demo for few stocks)
symbols = ["NSE:RELIANCE-EQ", "NSE:TCS-EQ", "NSE:INFY-EQ"]

today = dt.datetime.now().strftime("%Y-%m-%d")
start = today
end = today

rows = []
for sym in symbols:
    data = get_intraday(sym, "1", start, end)
    if "candles" not in data:  
        continue
    
    df = pd.DataFrame(data["candles"], columns=["time","open","high","low","close","volume"])
    
    # first 15-min high
    first_15m_high = df.iloc[:15]["high"].max()
    
    # % change from open to last close
    perc_change = ((df.iloc[-1]["close"] - df.iloc[0]["open"]) / df.iloc[0]["open"]) * 100
    
    crossed = "Yes" if df.iloc[-1]["close"] > first_15m_high and 2 <= perc_change <= 3 else "No"
    
    rows.append([sym, round(perc_change,2), first_15m_high, df.iloc[-1]["close"], crossed])

screener_df = pd.DataFrame(rows, columns=["Stock", "% Change", "15m High", "Last Close", "Crossed?"])

st.dataframe(screener_df)
