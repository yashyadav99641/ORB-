import streamlit as st
import pandas as pd
from fyers_helper import get_intraday, check_breakout

st.set_page_config(page_title="Nifty 500 Breakout Screener", layout="wide")
st.title("📊 Nifty 500 Breakout Screener")

symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]  # test list
results = []

for symbol in symbols:
    df = get_intraday(symbol)
    if df.empty:
        continue
    prev_close = df.iloc[0]["close"]
    signal = check_breakout(df, prev_close)
    if signal:
        results.append({"symbol": symbol, **signal})

if results:
    st.dataframe(pd.DataFrame(results))
else:
    st.info("No breakouts yet 🚦")
