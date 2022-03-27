import sys
sys.path.append('..')

import config.config_trade_conditions as conds
import config.config_paths as paths

from zaif_public_api_gateway import ZaifPublicApiGateway
from last_prices_store import LastPricesStore

def main():
    MAX_DATA_NUM = 60 * 24 * 7

    pub_api  = ZaifPublicApiGateway(conds.PAIR)
    data     = LastPricesStore(paths.CSV_DATA_PATH)

    last_price = pub_api.extract_last_price()

    data.enqueue_last_price(last_price)


    if data.count_last_prices() > MAX_DATA_NUM:
        data.dequeue_last_price()

    data.save_last_prices()





if __name__ == '__main__':
    main()
