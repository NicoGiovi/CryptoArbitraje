import requests
import asyncio
from binance import AsyncClient

async def main():

    # After we get all the data from binance trhough the client, we close the connection

    client = await AsyncClient.create()
    tickers = await asyncio.gather(client.get_all_tickers())
    await client.close_connection()

    # we proceed to filter all the tokens that are paired with USDT

    def filter_usdt_binance(ticker):
        if ticker['symbol'].endswith("USDT"):
            return ticker

    # then we clean all the None Values that left the map function

    binance_data = list(map(filter_usdt_binance, tickers[0]))
    binance_data = list(filter(lambda item: item is not None, binance_data))

    base_url_kucoin = "https://api.kucoin.com/api/v1/market/allTickers"
    resp = requests.get(url=base_url_kucoin).json()

    tickers = resp['data']['ticker']

    def filter_usdt_kucoin(ticker):
        if ticker['symbol'].endswith("USDT"):
            return {'symbol':ticker["symbol"].replace("-", ""), 'price': ticker['last']}

    kucoin_data = list(map(filter_usdt_kucoin, tickers))
    kucoin_data = list(filter(lambda item: item is not None, kucoin_data))

    # we match the price values for the same usdt paired tokens
    common_pairs = []

    for data_b in binance_data:
        for data_k in kucoin_data:
            if data_k['symbol'] == data_b['symbol']:
                common_pairs.append({'symbol':data_b['symbol'], 'price_b': data_b['price'], 'price_k':data_k['price']})


    # and we print in console the price difference in percentaje
    for pair in common_pairs:
        price_k = float(pair["price_k"])
        price_b = float(pair["price_b"])
        price_diff = ((price_k - price_b)/price_b)*100
        if price_diff < 99 and price_diff > -99:
            if price_diff > 1 or price_diff < -1:
                print(pair['symbol'], price_diff, "price_b", price_b, "price_k", price_k)

    # We will make in implementation of this script in Airflow or as an API web service
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
