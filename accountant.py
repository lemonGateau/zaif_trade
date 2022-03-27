from math import floor


class Accountant:
    def __init__(self, quotations, assets):
        """
        quotations: [bid, ask ]
        assets    : [jpy, coin]
        """
        self.bid_price  = quotations[0]
        self.ask_price  = quotations[1]
        self.jpy_asset  = assets[0]
        self.coin_asset = assets[1]

    def compute_total_assets(self):
        return int(self.jpy_asset + self.coin_asset * self.bid_price)

    def generate_bid_amount(self, min_amount=0.001, usage_rate=1.0):
        bid_amount = (self.jpy_asset * usage_rate) / self.bid_price

        return self._adjust_order_amount(bid_amount, min_amount)

    def generate_ask_amount(self, min_amount=0.001, usage_rate=1.0):
        ask_amount = self.coin_asset * usage_rate

        return self._adjust_order_amount(ask_amount, min_amount)

    def _adjust_order_amount(self, amount, min_amount=0.001):
        """ amountを注文最小単位のn倍に調整 """
        n = floor(amount / min_amount)

        return min_amount * n
