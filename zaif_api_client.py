import sys
sys.path.append('..')
import requests
import json
import time
import hmac
import hashlib
import urllib.parse


class ZaifApiClient:
    """ ユーザからは見えず、APIと直接やり取りするクラス """
    def __init__(self, pair):
        self.pair = pair
        self.public_end_point  = "https://api.zaif.jp/api/1"
        self.private_end_point = "https://api.zaif.jp/tapi"

        self.nonce = int(time.time())

    # ----- public api -----
    def _public_get(self, public_url):
        r = requests.get(public_url)

        return r.json()

    def fetch_pair_info(self):
        url = self.public_end_point + "/currency_pairs/" + self.pair

        return self._public_get(url)

    def fetch_last_price(self):
        """ ticker["last"] と同値 """
        url = self.public_end_point + "/last_price/" + self.pair

        return self._public_get(url)

    def fetch_ticker(self):
        url = self.public_end_point + "/ticker/" + self.pair

        return self._public_get(url)

    def fetch_depth(self):
        url = self.public_end_point + "/depth/" + self.pair

        return self._public_get(url)

    # ----- private api -----
    def set_api_keys(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def _generate_sign(self, params):
        sign = hmac.new(bytearray(self.secret_key.encode("utf-8")),\
            digestmod=hashlib.sha512)

        sign.update(params.encode("utf-8"))

        return sign.hexdigest()

    def _private_post(self, params):
        params = urllib.parse.urlencode(params)
        headers = {'key': self.access_key, 'sign': self._generate_sign(params)}

        r = requests.post(self.private_end_point, data=params, headers=headers)
        r = r.json()

        if r["success"]:
            return r["return"]

        print(r["return"])
        return

    def order(self, price, amount, action='bid'):
        self.nonce += 1

        params = {
        'method'       :'trade',
        'currency_pair': self.pair,
        'price'        : price,
        'amount'       : amount,
        'action'       : action,
        'nonce'        : str(self.nonce)
        }

        return self._private_post(params)

    def cancel_order(self, order_id):
        ''' 注文をキャンセル '''
        self.nonce += 1

        params = {
            'method'  : 'cancel_order',
            'order_id': order_id,
            'nonce'   : str(self.nonce)
        }

        return self._private_post(params)

    def fetch_active_orders(self):
        ''' 未約定の注文を取得 '''
        self.nonce += 1

        params = {
            'method': 'active_orders',
            'currency_pair': self.pair,
            'nonce': str(self.nonce)
        }

        return self._private_post(params)

    def fetch_funds(self):
        ''' 残高を取得 '''

        self.nonce += 1

        params = {
            'method': 'get_info2',
            'nonce': str(self.nonce)
        }

        return self._private_post(params)

    def fetch_trade_histories(self, count=1):
        ''' 取引履歴を取得 '''

        self.nonce += 1

        params = {
            'method': 'trade_history',
            'count': count,
            'currency_pair': self.pair,
            'nonce': str(self.nonce)
        }

        return self._private_post(params)
