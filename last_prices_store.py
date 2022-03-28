import pandas as pd
from datetime import datetime


class LastPricesStore:
    def __init__(self, csv_path):
        self.path = csv_path
        self.load_last_prices()

    def __del__(self):
        self.save_last_prices()

    def load_last_prices(self):
        self.lasts = pd.read_csv(self.path, header=0, names=["Date", "Last"])

    def enqueue_last_price(self, price):
        dt = str(datetime.now())
        self.lasts = self.lasts.append({"Date": dt, "Last": price}, ignore_index=True)

    def dequeue_last_price(self):
        self.lasts = self.lasts[1:]

    def save_last_prices(self):
        self.lasts.to_csv(self.path, index=False)

    def count_last_prices(self):
        return len(self.lasts["Last"])

    def generate_ohlc(self, interval="1H"):
        self.lasts["Date"] = pd.to_datetime(self.lasts["Date"])

        _lasts = self.lasts.groupby(pd.Grouper(key="Date", freq=interval))["Last"]

        bars = pd.DataFrame()
        bars["Open"]  = _lasts.first()
        bars["High"]  = _lasts.max()
        bars["Low"]   = _lasts.min()
        bars["Close"] = _lasts.last()

        bars.index = bars.index.tz_localize("UTC").tz_convert("Asia/Tokyo")

        return bars
