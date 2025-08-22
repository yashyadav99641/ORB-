import streamlit as st
import pandas as pd
import requests

st.title("Nifty 500 Screener 🚀")

st.write("This is a test app without fyers_helper")

# Example dummy dataframe
data = {
    "Stock": ["RELIANCE", "INFY", "TCS"],
    "% Change": [2.1, 2.5, 3.2],
    "Crossed First 15m High?": ["Yes", "No", "Yes"]
}

df = pd.DataFrame(data)
st.dataframe(df)
