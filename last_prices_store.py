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

        ohlc = pd.DataFrame()
        ohlc["Open"]  = _lasts.first()
        ohlc["High"]  = _lasts.max()
        ohlc["Low"]   = _lasts.min()
        ohlc["Close"] = _lasts.last()

        return ohlc
