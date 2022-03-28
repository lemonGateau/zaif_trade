try:
    from ..notifybot import LineNotifyBot
except:
    from notifybot import LineNotifyBot


class LineNotifier:
    def __init__(self, access_token):
        self.line_bot = LineNotifyBot(access_token)
        self.total_assets = None

    def notify_trade_history(self, price, amount, action="bid"):
        self.line_bot(f'{action}: {price}, {amount}')

    def notify_total_assets(self, total_assets):
        if self.total_assets is None:
            profit = 0
        else:
            profit = total_assets - self.total_assets

        self.line_bot.send(f'{total_assets}    {profit}')

        self.total_assets = total_assets
