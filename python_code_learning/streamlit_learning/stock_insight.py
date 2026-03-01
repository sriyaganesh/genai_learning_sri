import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.express as px
from io import StringIO
from flask import Flask, jsonify, request
from threading import Thread

# =========================
# DATA FUNCTIONS
# =========================

def load_nse_stocks():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    df = pd.read_csv(StringIO(r.text))
    return dict(zip(df["NAME OF COMPANY"], df["SYMBOL"]))


def get_last_10_days(symbol: str):
    symbol_y = symbol + ".NS"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_y}?range=15d&interval=1d"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    r = requests.get(url, headers=headers, timeout=10)

    data = r.json()
    result = data.get("chart", {}).get("result")
    if not result:
        return None

    timestamps = result[0]["timestamp"]
    closes = result[0]["indicators"]["quote"][0]["close"]

    records = []
    for t, c in zip(timestamps, closes):
        if c is not None:
            records.append({"Date": pd.to_datetime(t, unit="s"), "Close": c})

    return pd.DataFrame(records).tail(10)


def get_52_week(symbol: str):
    symbol_y = symbol + ".NS"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_y}?range=1y&interval=1d"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    r = requests.get(url, headers=headers, timeout=10)

    data = r.json()
    result = data.get("chart", {}).get("result")
    if not result:
        return None, None

    closes = result[0]["indicators"]["quote"][0]["close"]
    prices = [p for p in closes if p is not None]

    return round(max(prices), 2), round(min(prices), 2)


def analyze(prices):
    arr = np.array(prices)
    change_pct = (arr[-1] - arr[0]) / arr[0] * 100
    avg_price = arr.mean()
    high = arr.max()
    low = arr.min()
    volatility = arr.std() / avg_price * 100

    if change_pct > 3:
        signal = "BUY"
    elif change_pct < -3:
        signal = "AVOID"
    else:
        signal = "HOLD"

    return {
        "change_pct": round(change_pct, 2),
        "avg": round(avg_price, 2),
        "high": round(high, 2),
        "low": round(low, 2),
        "volatility": round(volatility, 2),
        "signal": signal,
    }


# =========================
# FLASK API
# =========================
app = Flask(__name__)

@app.route("/stock")
def stock_api():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "symbol required"}), 400

    df = get_last_10_days(symbol)
    if df is None or df.empty:
        return jsonify({"error": "no data"}), 404

    prices = df["Close"].tolist()
    stats = analyze(prices)
    high52, low52 = get_52_week(symbol)

    return jsonify({
        "dates": df["Date"].astype(str).tolist(),
        "prices": prices,
        "stats": stats,
        "high52": high52,
        "low52": low52
    })


def run_flask():
    app.run(port=5000)


# start flask once
if "flask_started" not in st.session_state:
    Thread(target=run_flask, daemon=True).start()
    st.session_state.flask_started = True


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Stock Insight", layout="centered")
st.title("📈 Stock Insight Dashboard")

# load stock list cached in UI
@st.cache_data(ttl=86400)
def cached_stocks():
    return load_nse_stocks()

STOCK_OPTIONS = cached_stocks()

stock_name = st.selectbox(
    "Search NSE Stock",
    list(STOCK_OPTIONS.keys()),
    index=None,
    placeholder="Type company name..."
)

if st.button("Get Stock Insight"):
    if not stock_name:
        st.warning("Please select a stock")
    else:
        symbol = STOCK_OPTIONS[stock_name]

        try:
            r = requests.get("http://localhost:5000/stock", params={"symbol": symbol}, timeout=10)
            data = r.json()

            if "error" in data:
                st.error(data["error"])
                st.stop()

            dates = pd.to_datetime(data["dates"])
            prices = data["prices"]
            stats = data["stats"]
            high52 = data["high52"]
            low52 = data["low52"]
            current_price = round(prices[-1], 2)

            df_prices = pd.DataFrame({"Date": dates, "Close": prices})

            st.markdown("### 📊 Stock Insights")

            # KPI GRID
            row1 = st.columns(3)
            row1[0].metric("Current Price (₹)", current_price)
            row1[1].metric("10-Day Change (%)", stats["change_pct"])
            row1[2].metric("Signal", stats["signal"])

            row2 = st.columns(3)
            row2[0].metric("52W High", high52)
            row2[1].metric("52W Low", low52)
            row2[2].metric("Volatility %", stats["volatility"])

            row3 = st.columns(3)
            row3[0].metric("10D High", stats["high"])
            row3[1].metric("10D Low", stats["low"])
            row3[2].metric("Average Price", stats["avg"])

            st.divider()

            # CHART
            st.subheader("10-Day Closing Price Trend")

            fig = px.line(
                df_prices,
                x="Date",
                y="Close",
                markers=True,
                title=f"{stock_name} — 10 Day Price Trend",
                labels={"Date": "Trading Date", "Close": "Closing Price (₹)"}
            )

            fig.update_layout(height=360, hovermode="x unified")
            fig.update_traces(
                hovertemplate=(
                    "<b>Stock:</b> " + stock_name +
                    "<br><b>Date:</b> %{x|%d-%b-%Y}" +
                    "<br><b>Price:</b> ₹%{y:.2f}"
                )
            )

            st.plotly_chart(fig, width="stretch")

            # INSIGHT
            st.subheader("Insight")
            if stats["signal"] == "BUY":
                st.success("Price shows upward momentum over last 10 days.")
            elif stats["signal"] == "AVOID":
                st.error("Recent sessions show downward trend.")
            else:
                st.warning("Price moving sideways without strong trend.")

        except Exception as e:
            st.error(str(e))