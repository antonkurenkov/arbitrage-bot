import json
import ast


def sell():
    return 'sell'


def buy():
    return 'buy'


with open('find_log', 'r') as log:
    order = log.readline()
    # order = collections.defaultdict(list)

d = ast.literal_eval(order)

main_pair = d['BTC']
print(main_pair)
pairs = [pair for pair in main_pair.values()]
print(pairs)
print('####')

for p in pairs:

    DIR = p['price'] * p['amount']

    print(f"Dir: {DIR}", p)
    p['pair'] = '_'.join(reversed(p['pair'].upper().split('_')))
    p['price'] = 1 / p['price']
    p['amount'] = 1 / p['amount']

    REV = p['price'] * p['amount']

    print(f"Rev: {REV}", p, DIR * REV)

