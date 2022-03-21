from zaif_api_client import ZaifApiClient


class ZaifPublicApiGateway:
    """ APIから得たデータを加工して、ユーザに提供するクラス """
    def __init__(self, pair):
        self.pair   = pair
        self.client = ZaifApiClient(pair)

    def extract_assets(self):
        funds = self.client.fetch_funds()

        jpy_asset  = funds["deposit"][self.pair.split("_")[1]]
        coin_asset = funds["deposit"][self.pair.split("_")[0]]

        return jpy_asset, coin_asset

    def extract_minimize_amount(self):
        r = self.client.fetch_pair_info()

        return r[0]["item_unit_min"]

    def extract_last_price(self):
        r = self.client.fetch_last_price()

        return r["last_price"]

    def extract_quotations(self):
        """ extract_depth_prices(0) と同値 """
        r = self.client.fetch_ticker()

        return r["bid"], r["ask"]

    def extract_depth_prices(self, depth_num):
        """ 板のboard_num番目の価格を取得 """
        r = self.client.fetch_depth()

        return r["bids"][depth_num][0], r["asks"][depth_num][0]


