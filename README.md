# CryptoArbitraje
Example of an ETL in python

Requisites:

-binance-python
-requests

In this example we wil extract data from two diferent exchanges (binance and kucoin) to make a comparision in the prices of all the usdt paired tokens. We will use two diferent methods:

- From Binance we will use the python wrapper
- From Kucoin we will extract the data using the exchanges's API

Then we will transform the raw data from both exchanges into a dictionary to match all the common pairs

And finally we will calculate the price diference and temporarily print it out in the console. Later we will implement it as an API of our own, or as a AirFlow Script

