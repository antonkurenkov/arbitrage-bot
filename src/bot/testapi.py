from poloniex import Poloniex

import time

api_key = 'MCEDZWVL-Z7RGQLRV-NWT35H79-QKP8XRLA'
api_secret = 'b8e2f2032edf721496d4c2682c69a883b0dd146b89eb3d84b736a4c66e3a00455fab13167bd9411187789d0ebd532ffd0cffc78005b9551b45150db4f5d45878'


def logging(deal):
    with open('trade_log', 'a') as log:
        log.write(str(deal))
        log.write('\n')

def api_buy():
    total = available_selling_amount * (1 / available_selling_rate)
    if total > 0.0001:
        deal = polo.buy(currencyPair=pair.upper(), rate=(1 / available_selling_rate), amount=total)
        print(deal)
        logging(deal)

    else:
        print(f'less, {total}')

def api_sell():
    deal = polo.sell(currencyPair=pair.upper(), rate=available_buying_rate, amount=available_buying_amount)
    print(deal)
    logging(deal)

if __name__ == '__main__':
    pair = 'usdt_btc'

    polo = Poloniex(api_key, api_secret)

    # print(f'{time.time()} Waiting...')
    balances = [0.0, 0.0]
    balances[0] = polo.returnBalances()[pair.split('_')[0].upper()]
    balances[1] = polo.returnBalances()[pair.split('_')[1].upper()]
    print(f'I: {balances}')
    orderbook = polo.returnOrderBook()
    print(orderbook[pair.upper()]['asks'])  # sells
    print(orderbook[pair.upper()]['bids'])  # buys

    # print(type(balances))

    available_selling_rate = float(orderbook[pair.upper()]['asks'][0][0])
    available_buying_rate = float(orderbook[pair.upper()]['bids'][0][0])
    # print(available_selling_rate)
    # print(available_buying_rate)

    available_selling_amount = orderbook[pair.upper()]['asks'][0][1] if orderbook[pair.upper()]['asks'][0][1] < \
                                                                        balances[0] else balances[0]
    available_buying_amount = orderbook[pair.upper()]['bids'][0][1] if orderbook[pair.upper()]['bids'][0][1] < balances[
        1] else balances[1]
    # print(available_selling_amount)
    # print(available_buying_amount)

    # sell()
    # buy()

    balances[0] = polo.returnBalances()[pair.split('_')[0].upper()]
    balances[1] = polo.returnBalances()[pair.split('_')[1].upper()]
    print(f'O: {balances}')