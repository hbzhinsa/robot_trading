#%%
from scraping import real_time_price
import pandas as pd
import datetime
Crypto=['btc','eth','ltc', 'doge', 'xpr', 'ada', 'etc']
while(True):
    price=[]
    col=[]
    info=[]
    time_stamp=datetime.datetime.now()-datetime.timedelta(hours=1)
    time_stamp=time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    
    for crypto_code in Crypto:
        [crypto_name,  price, change, volume, advice_MA15min, price_range]= real_time_price(crypto_code)
        info.append(price)
        info.extend(change)
        info.extend([volume])
        info.extend([advice_MA15min])
        info.extend([price_range])
        
    col=[time_stamp]
    col.extend(info)
    df=pd.DataFrame(col)
    df=df.T
    print('scraping data at '+time_stamp +' @investing.com')
    df.to_csv('realtime_data.csv',mode='a', header=False)   
# %%
