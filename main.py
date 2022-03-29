import csv
import sys
sys.path.append('..')
import json
from datetime import *
import pandas as pd

import config.config_trade_conditions as conds
import config.config_indicators as inds
import config.config_keys as keys
import config.config_paths as paths


from zaif_public_api_gateway import ZaifPublicApiGateway
from zaif_private_api_gateway import ZaifPrivateApiGateway
from accountant import Accountant
from last_prices_store import LastPricesStore
from line_notifier import LineNotifier

try:
    from ..indicators import *
    from ..cryptowatch import CryptowatchApi
    from ..yahoo_finance import YahooFinance
except:
    from indicators import *
    from cryptowatch import CryptowatchApi
    from yahoo_finance import YahooFinance


def main():
    pub_api  = ZaifPublicApiGateway(conds.PAIR)
    prv_api = ZaifPrivateApiGateway(conds.PAIR, keys.ACCESS_KEY, keys.SECRET_KEY)

    quotations = pub_api.extract_depth_prices(depth_num=5)
    assets     = prv_api.extract_assets()

    acct = Accountant(quotations, assets)

    MIN_AMOUNT = pub_api.extract_minimize_amount()

    bid_amount = acct.generate_bid_amount(MIN_AMOUNT, conds.JPY_USAGE_RATE)
    ask_amount = acct.generate_ask_amount(MIN_AMOUNT)

    store = LastPricesStore(paths.CSV_DATA_PATH)

    bars = store.generate_ohlc(interval=conds.INTERVAL)

    crypto = CryptowatchApi("bitflyer", conds.PAIR.replace("_", ""))
    before = datetime.now()
    after  = before - timedelta(days=60)
    periods = 300

    bars = crypto.generate_ohlc(before, after, periods)
    print(bars)

    range    = "7d"
    interval = "5m"

    yahoo = YahooFinance(conds.PAIR.replace("_", "-").upper())
    bars = yahoo.generate_ohlc(range, interval)

    dmi = Dmi()
    dmi.generate_indicators(bars["Close"], bars["High"], bars["Low"], [inds.ADX_TERM, inds.ADXR_TERM])

    macd = CrossMacd()
    macd.generate_indicators(bars["Close"], [inds.SHORT_TERM, inds.LONG_TERM], inds.MACD_SIGNAL_TERM)

    fp = FinalizedProfit(bars["Close"])
    fp.generate_indicators(inds.PROFIT_RATIO, inds.LOSS_RATIO)

    strategy = CombinationStrategy([dmi], [macd, fp])

    notifier = LineNotifier(keys.LINE_ACCESS_TOKEN)
    notifier.notify_total_assets(acct.compute_total_assets())

if __name__ == '__main__':
    main()
