import csv
import sys
sys.path.append('..')
import json
from datetime import datetime
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
except:
    from indicators import *


def main():
    pub_api  = ZaifPublicApiGateway(conds.PAIR)
    prv_api = ZaifPrivateApiGateway(conds.PAIR, keys.ACCESS_KEY, keys.SECRET_KEY)

    quotations = pub_api.extract_quotations()
    #quotations = pub_api.extract_depth_prices(depth_num=4)

    assets= prv_api.extract_assets()

    acct = Accountant(quotations, assets)

    MIN_AMOUNT = pub_api.extract_minimize_amount()

    bid_amount = acct.generate_bid_amount(MIN_AMOUNT, conds.JPY_USAGE_RATE)
    ask_amount = acct.generate_ask_amount(MIN_AMOUNT)

    last_price = pub_api.extract_last_price()

    store = LastPricesStore(paths.CSV_DATA_PATH)

    ohlc = store.generate_ohlc(interval=conds.INTERVAL)

    notifier = LineNotifier(keys.LINE_ACCESS_TOKEN)
    notifier.notify_total_assets(acct.compute_total_assets())

    dmi = Dmi()
    dmi.compute_tr(ohlc["Close"], ohlc["High"], ohlc["Low"])
    dmi.compute_dms(ohlc["High"], ohlc["Low"])
    dmi.compute_dis(inds.ADX_TERM)
    dmi.compute_dx()
    dmi.compute_adx(inds.ADX_TERM)
    dmi.compute_adxr(inds.ADXR_TERM)

    macd = CrossMacd()
    macd.generate_macds(ohlc["Close"], [inds.SHORT_TERM, inds.LONG_TERM], inds.MACD_SIGNAL_TERM)

    fp = FinalizedProfit(ohlc["Close"], inds.PROFIT_RATIO, inds.LOSS_RATIO)

    strategy = CombinationStrategy([dmi], [macd, fp])


    for i in range(len(ohlc["Close"])):
        if strategy.should_buy(i):
            print("buy ", ohlc["Close"][i])
            strategy.set_latest_buy_price(ohlc["Close"][i])

        elif strategy.should_sell(i):
            print("sell", ohlc["Close"][i])
            strategy.set_latest_buy_price(None)


if __name__ == '__main__':
    main()
