import sys
sys.path.append('..')
import json
import pandas as pd

import config_indicators as conf
import config_keys as keys


from zaif_public_api_gateway import ZaifPublicApiGateway
from zaif_private_api_gateway import ZaifPrivateApiGateway
from accountant import Accountant
from data_strage import DataStrage
from notifier import Notifier

try:
    from ..indicators import *
except:
    from indicators import *


def main():
    PAIR = "btc_jpy"
    JPY_USAGE_RATE = 0.5
    GROUP_INTERVAL = "5min"

    pub_api  = ZaifPublicApiGateway(PAIR)
    prv_api = ZaifPrivateApiGateway(PAIR, keys.ACCESS_KEY, keys.SECRET_KEY)

    quotations = pub_api.extract_quotations()
    #quotations = pub_api.extract_depth_prices(depth_num=4)

    assets= prv_api.extract_assets()

    acct = Accountant(quotations, assets)

    total_assets = acct.compute_total_assets()
    print(total_assets)

    MIN_AMOUNT = pub_api.extract_minimize_amount()

    bid_amount = acct.generate_bid_amount(MIN_AMOUNT, JPY_USAGE_RATE)
    ask_amount = acct.generate_ask_amount(MIN_AMOUNT)

    last_price = pub_api.extract_last_price()

    strage = DataStrage()
    notifier = Notifier(keys.LINE_ACCESS_TOKEN)

    lasts = strage.load_csv("C:\\Users\\manab\\github_\\zaif2\\db\\close.csv")

    lasts["date"] = pd.to_datetime(lasts["date"])

    lasts_freq = lasts.groupby(pd.Grouper(key="date", freq=GROUP_INTERVAL))["last"]

    bars = pd.DataFrame()
    bars["Open"]  = lasts_freq.first()
    bars["Close"] = lasts_freq.last()
    bars["High"]  = lasts_freq.max()
    bars["Low"]   = lasts_freq.min()

    print(bars)

    dmi = Dmi()
    dmi.compute_tr(bars["Close"], bars["High"], bars["Low"])
    dmi.compute_dms(bars["High"], bars["Low"])
    dmi.compute_dis(conf.ADX_TERM)
    dmi.compute_dx()
    dmi.compute_adx(conf.ADX_TERM)
    dmi.compute_adxr(conf.ADXR_TERM)

    macd = CrossMacd()
    macd.generate_macds(bars["Close"], [conf.SHORT_TERM, conf.LONG_TERM], conf.MACD_SIGNAL_TERM)

    fp = FinalizedProfit(bars["Close"], conf.PROFIT_RATIO, conf.LOSS_RATIO)

    strategy = CombinationStrategy([dmi], [macd, fp])


    for i in range(len(bars["Close"])):
        if strategy.should_buy(i):
            print("buy ", bars["Close"][i])
            strategy.set_latest_buy_price(bars["Close"][i])

        elif strategy.should_sell(i):
            print("sell", bars["Close"][i])
            strategy.set_latest_buy_price(None)


if __name__ == '__main__':
    main()
