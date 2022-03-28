from zaif_api_client import ZaifApiClient


class ZaifPrivateApiGateway:
    """ APIから得たデータを加工して、ユーザに提供するクラス """
    def __init__(self, pair, access_key, secret_key):
        self.pair   = pair.lower()
        self.client = ZaifApiClient(pair)
        self.client.set_api_keys(access_key, secret_key)

    def extract_assets(self):
        funds = self.client.fetch_funds()

        coin_name, jpy = self.pair.split("_")

        jpy_asset  = funds["deposit"][jpy]
        try:
            coin_asset = funds["deposit"][coin_name]
        except:
            coin_asset = funds["deposit"][coin_name.upper()]

        return jpy_asset, coin_asset

    def extract_minimize_amount(self):
        r = self.client.fetch_pair_info()

        return r[0]["item_unit_min"]

    def execute_order(self, price, amount, action="bid"):
        return self.client.order(price, amount, action)

    def cancel_order(self, order_id):
        return self.client.cancel_order(order_id)

    def extract_active_orders(self):
        return self.client.fetch_active_orders()

    def extract_trade_histories(self, count=1):
        return self.client.fetch_trade_histories(count)

    