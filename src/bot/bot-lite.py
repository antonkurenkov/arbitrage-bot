import collections
import json
import time
from datetime import datetime
from poloniex import Poloniex

# COMMISSION = 0.0025
COMMISSION = 0

CONFIG_FILE = '../resources/pairs_old.json'
MAIN_ACTIVE = ['ETH']

api_key = '<your_api_key>'
api_secret = '<your_secret>'

class Trader():

    def __init__(self):

        with open(CONFIG_FILE) as f:
            self.pairs = json.load(f)
        self.polo = Poloniex(api_key, api_secret)
        self.balances = self.polo.returnBalances()

    def booking(self):

        order_book = self.polo.returnOrderBook(depth=1)
        dictionary = collections.defaultdict(dict)
        for pair in self.pairs:
            p = pair.upper()
            src, dst = p.split('_')
            ask_order = order_book[p]['asks'][0]
            src_ask = {
                'pair': src + '_' + dst,
                'price': float(ask_order[0]),
                'amount': float(ask_order[1])
            }
            bid_order = order_book[p]['bids'][0]
            src_bid = {
                'pair': dst + '_' + src,
                'price': 1 / float(bid_order[0]),
                'amount': float(bid_order[1]) * float(bid_order[0])
            }
            dictionary[src][dst] = src_ask
            dictionary[dst][src] = src_bid
        self.book = dictionary

def get_amount(mypolo, order_1, order_2, order_3):
    amount_3 = order_3['amount'] * order_3['price']

    amount_2 = order_2['amount'] if order_2['amount'] < amount_3 else amount_3
    amount_2 = amount_2 * order_2['price']

    return order_1['amount'] if order_1['amount'] < amount_2 else amount_2

    # return orders_amount if orders_amount < mypolo.balances[MAIN_ACTIVE[0]] else mypolo.balances[MAIN_ACTIVE[0]]


def trading(mypolo, kwargs):
    print(mypolo.book)
    for kw in kwargs:

        # print(mypolo.book)
        bal_I = mypolo.balances[kw['pair'].split('_')[0].upper()]
        # print(f'I: {bal_I}')
        bal_O = mypolo.balances[kw['pair'].split('_')[1].upper()]
        # print(f'O: {bal_O}')

        switch = False
        if kw['pair'].lower() not in mypolo.pairs:
            switch = True

            pair = '_'.join(reversed(kw['pair'].upper().split('_')))
            mybook = mypolo.book[pair.split('_')[1]][pair.split('_')[0]]
            price = mybook['price']
            amount = price * mybook['amount'] if price * mybook['amount'] < price * bal_I else price * bal_I

            # print(f"{kw['pair'], kw['price'], kw['amount'], switch}")
            print(f"{pair, price, amount, switch}")
            response = mypolo.polo.sell(pair, price, amount, immediateOrCancel=1)

        else:
            pair = kw['pair']

            mybook = mypolo.book[pair.split('_')[0]][pair.split('_')[1]]
            price = mybook['price']

            amount = price / mybook['amount'] if price / mybook['amount'] < bal_I else bal_I

            # print(f"{kw['pair'], kw['price'], kw['amount'], switch}")
            print(f"{pair, price, amount, switch}")
            response = mypolo.polo.buy(pair, price, amount, immediateOrCancel=1)  # BUY!!!

        print(response)

        with open('trade_log', 'a') as log:
            log.write(f'{str(response)}, switch={switch}')
            log.write('\n')

    # print('\n')
    # time.sleep(0.5)



def main(mypolo):
    # mypolo = Trader()

    # print(mypolo.book)
    # [print(item) for item in mypolo.book.items()]

    for active in MAIN_ACTIVE: #  ETH
        # print(f'active={active}')
        orders = mypolo.book
        for (currency_1, currencies_1) in orders.items():
            # print(f'    currency1={currency_1}')
            # print(f'    currencies1={currencies_1}')
            for (currency_2, order) in currencies_1.items():
                # print(f'        currency_2={currency_2}')
                # print(f'        order={order}')

                if currency_2 == active or currency_1 == active:
                    continue
                order_1 = orders[active][currency_1]
                order_2 = order
                order_3 = orders[currency_2][active]

                amount = get_amount(mypolo, order_1, order_2, order_3)
                order_price = order_1['price'] * amount

                transfer_1 = amount * (1 - COMMISSION)
                transfer_2 = transfer_1 / order_2['price'] * (1 - COMMISSION)
                transfer_3 = transfer_2 / order_3['price'] * (1 - COMMISSION)

                if (transfer_3 / order_price) > 1:
                    with open('find_log', 'a') as log:
                        log.write(f'{mypolo.book}')
                        log.write('\n')
                    trading(mypolo, [order_1, order_2, order_3])




if __name__ == '__main__':
    mypolo = Trader()
    while True:
        timer = datetime.now()
        try:
            mypolo.booking()
            main(mypolo)
        except Exception as inst:
            print(type(inst))  # the exception instance
            # print(inst.args)  # arguments stored in .args
            print(inst)
        end = datetime.now()
        total = end - timer
        print(f'\nDuration: {str(total)[5:]} secs')
        mypolo.balances = mypolo.polo.returnBalances()

