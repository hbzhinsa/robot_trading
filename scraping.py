#%%
import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

#https://www.youtube.com/watch?v=q_MWWVgghsQ&t=151s
# very good tutorial
#
# 
url_mining_difficulty='https://www.coinwarz.com/charts/difficulty-charts'
url_top_profit='https://www.coinwarz.com/cryptocurrency?sort=profitusd&dir=desc'
def real_time_price(crypto_name='btc'):
    def crypto(name):
        name=name.lower()
        switcher={
                'eth':'https://www.investing.com/crypto/ethereum/eth-usd',
                'btc':'https://www.investing.com/crypto/bitcoin/btc-usd',
                'ltc':'https://www.investing.com/crypto/litecoin/ltc-usd',
                'iot':'https://www.investing.com/crypto/iota/iota-usd',
                'xpr':'https://www.investing.com/crypto/xrp/xrp-usd',
                'ada':'https://www.investing.com/crypto/cardano/ada-usd',
                'etc':'https://www.investing.com/crypto/ethereum-classic/etc-usd',
                'doge':'https://www.investing.com/crypto/dogecoin/doge-usd',
                'sol': 'https://www.investing.com/crypto/solana/sol-usd',
                'bch':'https://www.investing.com/crypto/bitcoin-cash/bch-usd', 
                'zec':'https://www.investing.com/crypto/zcash/zec-usd'
             }
        return switcher.get(name,"will be added if needed")
    url=crypto(crypto_name)
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    class_name='instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold'
    price=soup.find('div', {'class': class_name}).find_all('span')[0].text
    change=soup.find('div', {'class': class_name}).find_all('span')[1].text
    change_percent=soup.find('div', {'class': class_name}).find_all('span')[2].text
    volume=soup.find('div', {'data-test':'volume-value'}).text
    #class_name='datatable_cell__3gwri datatable_cell--up__2984w instrument-tech-summary_table-cell__2JiYj'
    class_name='datatable_cell__3gwri datatable_cell--down__2CL8n instrument-tech-summary_table-cell__2JiYj'
    advice=soup.find('tr', {'data-test':"instrument-tech-table-row" })
    advice_MA15min=advice.find_all('td')[2].text
    price_range=soup.find('div', {'data-test':'range-value'}).text
    return [crypto_name,  price, [change+' '+(change_percent)], volume, advice_MA15min, price_range] 

def test_read():
    x=real_time_price()
    return {'crypto_name': x[0], 'current price': x[1], 'change': x[2], 'volume': x[3], 
            'advice(15 mean average)':x[4] , 'price range': x[5]}
    
test_read()  
  


# %%
