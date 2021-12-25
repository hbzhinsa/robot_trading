#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import datetime
import math
import warnings
import requests
from bs4 import BeautifulSoup

# %%
warnings.simplefilter(action='ignore', category=FutureWarning)
Crypto=['BTC','ETH','LTC', 'DOGE', 'BCH', 'ZEC', 'ETC']
fig=plt.figure() #figsize=(50,25)
fig.set_size_inches(15.5, 8.5)
fig.patch.set_facecolor('#121416')
gs=fig.add_gridspec(6,6)
ax1=fig.add_subplot(gs[0:4,0:4])
ax2=fig.add_subplot(gs[0,4:6])
ax3=fig.add_subplot(gs[1,4:6])
ax4=fig.add_subplot(gs[2,4:6])
ax5=fig.add_subplot(gs[3,4:6])
ax6=fig.add_subplot(gs[4,4:6])
ax7=fig.add_subplot(gs[5,4:6])
ax8=fig.add_subplot(gs[4,0:4])
ax9=fig.add_subplot(gs[5,0:4])

def figure_design(ax):
    ax.set_facecolor('#091217')
    ax.tick_params(axis='both', labelsize=14,colors='white')
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#808080')
    ax.spines['top'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')

def subplot_plot(ax, stock_code, data, latest_price, latest_change, pattern, range52):
    ax.clear()
    ax.plot(list(range(1,len(data['close'])+1)), data['close'], color='white', linewidth=2)
    ymin=data['close'].min()
    ymax=data['close'].max()
    ystd=data['close'].std()
    if not math.isnan(ymax) and not math.isnan(ystd) and ymax!=0:
        try:
            ax.set_ylim([ymin-ystd*0.5, ymax+ystd*3])
        except ValueError:
            print('set y limit later with more data')           
    ax.text(0.02,0.95,stock_code, transform=ax.transAxes,color='#FFBF00', fontsize=11,fontweight='bold',
    horizontalalignment='left', verticalalignment='top') 
       
    ax.text(0.2,0.95,latest_price, transform=ax.transAxes,color='white', fontsize=9,fontweight='bold',
    horizontalalignment='left', verticalalignment='top')  
    if latest_change[0] =='+':
        colorcode='#18b800'
    else:
        colorcode='#ff3503' 
              
    ax.text(0.4,0.95,latest_change, transform=ax.transAxes,color=colorcode, fontsize=9,fontweight='bold',
    horizontalalignment='left', verticalalignment='top')      
    
    if 'Buy' in pattern:
        colorcode='#18b800'
    elif 'Sell' in pattern:
        colorcode='#ff3503'
    else:
        colorcode='white'

    ax.text(0.98,0.95,pattern, transform=ax.transAxes,color=colorcode, fontsize=9,fontweight='bold',
    horizontalalignment='right', verticalalignment='top') 
    ax.text(0.98,0.75,range52, transform=ax.transAxes,color='#08a0e9', fontsize=9,fontweight='bold',
    horizontalalignment='right', verticalalignment='top') 
    figure_design(ax)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
           


def str_to_number(df, column):
    if isinstance(df.iloc[0, df.columns.get_loc(column)], str):
        df[column]=df[column].str.replace(',', '')
        df[column]=df[column].astype(float)
    return df 

def computeRSI(data, time_window): #14
    diff=data.diff(1).dropna()
    up_chg=0*diff
    down_chg=0*diff
    up_chg[diff>0]=diff[diff>0]
    down_chg[diff<0]=diff[diff<0]
    up_chag_ave=up_chg.ewm(com=time_window-1,min_periods=time_window).mean()
    down_chag_ave=down_chg.ewm(com=time_window-1,min_periods=time_window).mean()
    rs=abs(up_chag_ave/down_chag_ave)
    rsi=100-100/(1+rs)
    return rsi


def read_data_ohlc(filename, stock_code, usecols):
    df=pd.read_csv(filename, header=None, usecols=usecols, 
                   names=['time',stock_code,'change','volume','pattern','range'], 
                   index_col='time',parse_dates=['time'] ) 
    index_with_nan=df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan, 0, inplace=True)
    df.index=pd.DatetimeIndex(df.index)
    df=str_to_number(df, stock_code)
    df=str_to_number(df, 'volume')
    latest_info=df.iloc[-1,:]
    latest_price=str(latest_info[0])
    
    change=str(latest_info[1])
    change_num= change.rsplit(' ', 1)[0]
    change_per=change.rsplit(' ', 1)[1]
    rounded_change=round(float(change_num.replace(',', '')),3)
    latest_change=change[0]+str(rounded_change)+' '+change_per
    

    df_vol=df['volume'].resample('1Min').mean()
    data=df[stock_code].resample('1Min').ohlc()

    data['time']=data.index
    data['time']=pd.to_datetime(data['time'],format='%Y-%m-%d %H:%M:%S')
    data['MA5']=data['close'].rolling(5).mean()
    data['MA10']=data['close'].rolling(10).mean()
    data['MA20']=data['close'].rolling(20).mean()
    data['RSI']=computeRSI(data['close'], 14)
    data['volume_diff']=df_vol.diff()
    data[data['volume_diff']<0]=None
    index_with_nan=data.index[data.isnull().any(axis=1)]
    data.drop(index_with_nan, 0, inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data, latest_price, latest_change, df['pattern'][-1], df['range'][-1], df['volume'][-1]
    



#%%
    

filename='realtime_data.csv'
# data, latest_price, latest_change, pattern, range52, volume=\
#     read_data_ohlc(filename,Crypto[0].lower(), [1,2,3,4,5,6])


#%%

# %%
def animate(i): 
    data, latest_price, latest_change, pattern, range52, volume=\
    read_data_ohlc(filename,Crypto[0].lower(), [1,2,3,4,5,6])
    candle_counter=range(len(data['open'])-1)
    ohlc=[]
    for candle in candle_counter:
        append_me=candle_counter[candle],data['open'][candle],  \
            data['high'][candle], data['low'][candle], \
                data['close'][candle]   
        ohlc.append(append_me)
    ax1.clear()
    
    candlestick_ohlc(ax1,ohlc,width=0.4,colorup='#18b800', colordown='#ff3503')
    ax1.plot(data['MA5'], color='pink', linestyle='-', linewidth=1, label='5 mins SMA')
    ax1.plot(data['MA10'], color='orange', linestyle='-', linewidth=1, label='10 mins SMA')
    ax1.plot(data['MA20'], color='#08a0e9', linestyle='-', linewidth=1, label='20 mins SMA')
    leg=ax1.legend(loc='upper left', facecolor='#121416', fontsize=10)
    for text in leg.get_texts():
        plt.setp(text,color='w')
    figure_design(ax1)
    ax1.text(0.005,1.05,Crypto[0], transform=ax1.transAxes,color='black', fontsize=16, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center', 
                bbox=dict(facecolor='#FFBF00'))


    if latest_change[0]=='+':
        colorcode='#18b800'
    else:
        colorcode='#ff3503'

    ax1.text(0.2,1.05, latest_price, transform=ax1.transAxes, color='white', fontsize=12, 
                fontweight='bold', horizontalalignment='center', verticalalignment='center')
    ax1.text(0.5,1.05, latest_change, transform=ax1.transAxes, color=colorcode, fontsize=12, 
                fontweight='bold', horizontalalignment='center', verticalalignment='center')

    url='https://www.coinwarz.com/mining/bitcoin/difficulty-chart'
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text=soup.find('p', {'class':'small muted'}).text
    dflty_btc=text[30:37]
    
    url='https://www.coinwarz.com/cryptocurrency'
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text1=soup.find('div', {'style':'float: left; min-width: 200px;'}).find('div', {'style':'margin-bottom:10px;'}).text
    rank1=text1.replace(' ','').replace('\n','').replace('\r', '')
    profit1=soup.find('span', {'style':'font-size:36px; font-weight:bold;color:#000;'}).text
    
    ax1.text(1.3, 1.05,'Top Mining Profit :'+rank1+' '+profit1, transform=ax1.transAxes, color='white', fontsize=10, fontweight='bold',
             horizontalalignment='center', verticalalignment='center')
    
    ax1.text(0.65,1.1, 'Mining Difficulty:', transform=ax1.transAxes, color='white', fontsize=12, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center')
    
    ax1.text(0.9,1.1, text[30:37], transform=ax1.transAxes, color='white', fontsize=12, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center')
    
    
    if 'Buy' in pattern:
        colorcode='#18b800'
    elif 'Sell' in pattern:
        colorcode='#ff3503'
    else:
        colorcode='white'
    ax1.text(0.65,1.05, '15min SMA :', transform=ax1.transAxes, color='white', fontsize=12, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center')
    
    ax1.text(0.9,1.05, pattern, transform=ax1.transAxes, color=colorcode, fontsize=12, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center')
    ax1.text(0.75,0.95, 'Day range', transform=ax1.transAxes, color='white', fontsize=10, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center')
    ax1.text(0.75,0.9, range52, transform=ax1.transAxes, color='white', fontsize=10, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center')

    time_stamp=datetime.datetime.now()
    time_stamp=time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    ax1.text(1.3, 1.1,time_stamp, transform=ax1.transAxes, color='white', fontsize=12, fontweight='bold',
             horizontalalignment='center', verticalalignment='center')
    ax1.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
    ax1.set_xticklabels([])

    data_ax2, latest_price2, latest_change2, pattern2, range522, volume2=\
        read_data_ohlc(filename,Crypto[1].lower(), [1,7,8,9,10,11])
    subplot_plot(ax2, Crypto[1], data_ax2,latest_price2, latest_change2, pattern2, range522)

    data_ax3, latest_price3, latest_change3, pattern3, range523, volume3=\
        read_data_ohlc(filename,Crypto[2].lower(), [1,12,13,14,15,16])
    subplot_plot(ax3, Crypto[2], data_ax3,latest_price3, latest_change3, pattern3, range523)  

    data_ax4, latest_price4, latest_change4, pattern4, range524, volume4=\
        read_data_ohlc(filename,Crypto[3].lower(), [1,17,18,19,20,21])
    subplot_plot(ax4, Crypto[3], data_ax4,latest_price4, latest_change4, pattern4, range524) 
   
    data_ax5, latest_price5, latest_change5, pattern5, range525, volume5=\
        read_data_ohlc(filename,Crypto[4].lower(), [1,22,23,24,25,26])
    subplot_plot(ax5, Crypto[4], data_ax5,latest_price5, latest_change5, pattern5, range525)   

    data_ax6, latest_price6, latest_change6, pattern6, range526, volume6=\
        read_data_ohlc(filename,Crypto[5].lower(), [1,27,28,29,30,31])
    subplot_plot(ax6, Crypto[5], data_ax6,latest_price6, latest_change6, pattern6, range526)
        
    data_ax7, latest_price7, latest_change7, pattern7, range527, volume7=\
        read_data_ohlc(filename,Crypto[6].lower(), [1,32,33,34,35,36])   
    subplot_plot(ax7, Crypto[6], data_ax7,latest_price7, latest_change7, pattern7, range527)
    
    ax8.clear()
    figure_design(ax8)
    ax8.axes.yaxis.set_visible(False)
    pos=data['open']-data['close']<0
    neg=data['open']-data['close']>0
    data['x_axis']=list(range(1,len(data['volume_diff'])+1))
    ax8.bar(data['x_axis'][pos],data['volume_diff'][pos],color='#18b800', width=0.8, align='center')
    ax8.bar(data['x_axis'][neg],data['volume_diff'][neg],color='#ff3503', width=0.8, align='center') 
    ymax=data['volume_diff'].max()
    ystd=data['volume_diff'].std()
    if not math.isnan(ymax):
        ax8.set_ylim([0,ymax+ystd*3])
    ax8.text(0.01,0.95,'Volume :'+'{:,}'.format(int(volume)), transform=ax8.transAxes, color='white',
             fontsize=10, fontweight='bold', horizontalalignment='left', verticalalignment='top')
    ax8.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
    ax8.set_xticklabels([])
    
    ax9.clear()
    figure_design(ax9)
    ax9.axes.yaxis.set_visible(False)
    ax9.set_ylim([-5, 105])
    ax9.axhline(30, linestyle='-', color='green', linewidth=0.5)
    ax9.axhline(50,linestyle='-', color='white', linewidth=0.5)
    ax9.axhline(70, linestyle='-', color='red', linewidth=0.5)
    ax9.plot(data['x_axis'], data['RSI'], color='#08a0e9',linewidth=1.5)
    ax9.text(0.01,0.95,'RSI(14):'+str(round(data['RSI'].iloc[-1], 2)), transform=ax9.transAxes, color='white',
             fontsize=10, fontweight='bold', horizontalalignment='left', verticalalignment='top')
    xdate=[i for i in data['time']]
    def mydate(x,pos=None):
        try:
            t=xdate[int(x)].strftime('%H:%M')
            return t
        except IndexError:
            return ''
    ax9.xaxis.set_major_formatter(mticker.FuncFormatter(mydate))
    ax9.grid(True,color='grey', linestyle='-', which='major', axis='both',linewidth=0.3)
    ax9.tick_params(axis='x', which='major',labelsize=10 )
    


    

#%%

ani=animation.FuncAnimation(fig,animate, interval=1)
plt.show()
# %%
