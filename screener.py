import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AAPL", "MSFT", "TSLA", "AMZN", "NVDA", "JPM", "GS", "BAC", "V", "META"]

data = []

for stock in stocks:
    try:
        info = yf.Ticker(stock).info
        history = yf.Ticker(stock).history(period="1y")

        annual_return = ((history["Close"].iloc[-1] - history["Close"].iloc[0]) / history["Close"].iloc[0]) * 100
        volatility = history["Close"].pct_change().std() * 100

        data.append({
            "Ticker": stock,
            "Price": round(info.get("currentPrice", 0), 2),
            "P/E Ratio": round(info.get("trailingPE", 0), 1),
            "1Y Return (%)": round(annual_return, 1),
            "Volatility (%)": round(volatility, 2),
            "Market Cap ($B)": round(info.get("marketCap", 0) / 1e9, 1)
        })
        print("Fetched: " + stock)

    except:
        print("Skipped: " + stock)

df = pd.DataFrame(data)
df = df.sort_values("1Y Return (%)", ascending=False).reset_index(drop=True)

print("\n--- Stock Screener Results ---\n")
print(df.to_string(index=False))
df.to_csv("/Users/ryandonsky/Desktop/screener_results.csv", index=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

colors = ["#1D9E75" if x > 0 else "#E24B4A" for x in df["1Y Return (%)"]]
ax1.barh(df["Ticker"], df["1Y Return (%)"], color=colors)
ax1.set_title("1 Year Return (%)")
ax1.set_xlabel("Return (%)")
ax1.axvline(x=0, color="black", linewidth=0.5)

ax2.scatter(df["P/E Ratio"], df["1Y Return (%)"], color="#378ADD", s=100)
for i, row in df.iterrows():
    ax2.annotate(row["Ticker"], (row["P/E Ratio"], row["1Y Return (%)"]),
                textcoords="offset points", xytext=(6, 4), fontsize=9)
ax2.set_title("P/E Ratio vs 1Y Return")
ax2.set_xlabel("P/E Ratio")
ax2.set_ylabel("1Y Return (%)")

plt.tight_layout()
plt.savefig("/Users/ryandonsky/Desktop/screener_chart.png")
plt.show()
print("Chart saved to Desktop")