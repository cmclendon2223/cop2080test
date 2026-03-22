import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Info")

st.title("Crypto Info")

coin = st.sidebar.selectbox("Select a crypto: ", ["bitcoin", "dogecoin"])

days = st.sidebar.slider("Range (days): ", min_value=1, max_value=90, value=30)

@st.cache_data
def getMarketData():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc","per_page": 10}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@st.cache_data
def getHistoricalData(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd","days": days}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


try:
    marketData = getMarketData()
    histData = getHistoricalData(coin, days)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()


dfMarket = pd.DataFrame(marketData)

prices = histData["prices"]
dfHist = pd.DataFrame(prices, columns=["timestamp", "price"])
dfHist["timestamp"] = pd.to_datetime(dfHist["timestamp"], unit="ms")
selectedCoinData = dfMarket[dfMarket["id"] == coin].iloc[0]

st.subheader(coin.capitalize() + "Price Over Time: ")
st.line_chart(dfHist.set_index("timestamp")["price"])

st.subheader("Metrics: ")
col1, col2, col3 = st.columns(3)
col1.metric("Current Price $:", f"${selectedCoinData['current_price']:,}")
col2.metric("Daily Change (%)", f"{selectedCoinData['price_change_percentage_24h']:.2f}%")
col3.metric("Market Cap $: ", f"${selectedCoinData['market_cap']:,}")

st.subheader("Market Cap $: ")
bar_df = pd.DataFrame({"name": [selectedCoinData["name"]], "market_cap": [selectedCoinData["market_cap"]]}).set_index("name")
st.bar_chart(bar_df)
