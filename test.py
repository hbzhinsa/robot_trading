#%%
import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


# url='https://www.coinwarz.com/mining/bitcoin/difficulty-chart'
# url='https://www.coinwarz.com/mining/ethereum/difficulty-chart'
# url='https://www.coinwarz.com/mining/litecoin/difficulty-chart'
# url='https://www.coinwarz.com/mining/dogecoin/difficulty-chart'
# url='https://www.coinwarz.com/mining/bitcoincash/difficulty-chart'
# url='https://www.coinwarz.com/mining/zcash/difficulty-chart'
# url='https://www.coinwarz.com/mining/ethereum-classic/difficulty-chart'
url='https://www.coinwarz.com/cryptocurrency'
r=requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
text1=soup.find('div', {'style':'float: left; min-width: 200px;'}).find('div', {'style':'margin-bottom:10px;'}).text
rank1=text1.replace(' ','').replace('\n','').replace('\r', '')

text2=soup.find('span', {'style':'font-size:36px; font-weight:bold;color:#000;'}).text

# %%
