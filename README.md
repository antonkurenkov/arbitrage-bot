# Arbitrage bot
Arbitrage bot in poloniex stock exchange. Finds arbitrage situations between three types of currencies.
For example: BTC => ETH => ETC => BTC.

Input your API and your secret keys. The bot would even try to catch this situations and trade on them. 

To be fair the speed of this bot is quite not enough for both three transactions to be processed. That's why this project was deadborn.

## Run
* Download python3;
* Run **setup.sh** script in terminal - `sudo sh setup.sh`;
* Move to **src** folder and run main.py - `sudo python3 main.py`.

## Structure
* Resources folder store filed **pairs.json** with currency pairs;
* Bot folder store bot code.
