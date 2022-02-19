# ticker details DailyLoad Import
import pyodbc
import pandas as pd
import timedelta as dtdel # this need to be installed . This will get the date difference 
import time as t
import config_amtrade_plus_plus 
import datetime as dtm
import alpaca_trade_api as tradeapi
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

print('process started at '+ str(dtm.datetime.now()))


#test
print(type(config_amtrade_plus_plus.alpaca_paper_secret_key))



#Setup alpaca api . This will be used in all transactions
#Here the setup is for the paper trading account.Similar can be setup for the live account 
api_paper = tradeapi.REST(key_id=config_amtrade_plus_plus.alpaca_paper_key_id,secret_key=config_amtrade_plus_plus.alpaca_paper_secret_key,base_url='https://paper-api.alpaca.markets')
#api_paper.get_account()
#api_paper.get_account_configurations()



#This Block will get the dates to be used in the function. It will get the start date and the end date whichw ill contaion latest 30 trading days
#It will pick last 60 days of the dates from today.The final goal is to extract last 30 days of trading 
#dates which will definitely in between 60 days 
end_dt = dtm.date.today()
start_dt = end_dt - dtdel.Timedelta(days=60)

#this will get the actual tradings days in last 60  cal days.Ex. Out of last 60 previous cal days there are 30 cal days
caln = api_paper.get_calendar(start=start_dt,end=end_dt) 

#As the output will be in the list formart , that can be converted to the dataframe with below syntax.
#After that the date can be extracted from the df 

calnDf = pd.DataFrame({                          
         'close': [x.close for x in caln],
         'date': [x.date for x in caln],
         'open': [x.open for x in caln],
         'session_close': [x.session_close for x in caln],
         'session_open': [x.session_open for x in caln]
        })

#The start date is the date after which 3 trading days happned inculding the date.
prev_30_start_dt=str(calnDf[-30:-29]['date'].values[0])[:10]

print('start_dt :'+prev_30_start_dt)
print('end_dt   :'+ str(end_dt))




def getAllActiveTrades(active_interested_assets_df,prev_30_start_dt,end_dt):
    try:
                        
        #This will get the history data of the perticular stock for last 30 days 
        r=api_paper.get_bars(symbol=active_interested_assets_df['symbol'],timeframe='1Day',start=prev_30_start_dt,end=end_dt).df
        
        
        #This will be the dictionaly which will have all the information need to be returend for the next level of calculation
        #avg_lstday_details= {'last_eod_price':r['close'][-1],'last_eod_volume':r['volume'][-1],'avg_30_day_price':r['close'].mean(),'avg_30_day_volume':r['volume'].mean() }
        
        avg_lstday_details=active_interested_assets_df.append(
            pd.Series([
            r['close'][-1],
            r['volume'][-1],
            r['close'].mean(),
            r['volume'].mean()],
            index=['last_eod_price', 'last_eod_volume', 'avg_30_day_price', 'avg_30_day_volume']))
        #avg_lstday_details=pd.Series([r['close'][-1],r['volume'][-1],r['close'].mean(),r['volume'].mean()],index=['last_eod_price', 'last_eod_volume', 'avg_30_day_price', 'avg_30_day_volume'])
        #print(avg_lstday_details['symbol'])
        #print(avg_lstday_details)
        return avg_lstday_details
    
    except Exception as e:
        print (str(e)+'-ERRORRRR Occured ')

#This is to get all the assents from alpaca 
active_assets = api_paper.list_assets()
#active_assets
active_assets_df = pd.DataFrame({                          
         'easy_to_borrow': [x.easy_to_borrow for x in active_assets],
         'exchange': [x.exchange for x in active_assets],
         'fractionable': [x.fractionable for x in active_assets],
         'id': [x.id for x in active_assets],
         'marginable': [x.marginable for x in active_assets],
         'name': [x.name for x in active_assets],
         'shortable': [x.shortable for x in active_assets],
         'status': [x.status for x in active_assets],
         'symbol': [x.symbol for x in active_assets],
         'tradable': [x.tradable for x in active_assets]
        })
#active_assets_df

#Get the assents we are interested in 
active_interested_assets_df=active_assets_df[((active_assets_df['exchange']=='NYSE')  |   (active_assets_df['exchange']=='NASDAQ')) 
               & 
                 (active_assets_df['status']=='active')]#.iloc[0:20]
#active_interested_assets_df

#Call the function to calculate teh mast price volume along with the 30 day average
active_interested_assets_df=active_interested_assets_df.apply(getAllActiveTrades,args=(prev_30_start_dt,end_dt),axis=1)
print('Data collectd from alpacta')

#Get the not null symbols to be laoded to the database 
db_active_interested_assets_df=active_interested_assets_df[~active_interested_assets_df['symbol'].isnull()]
#CName is requried as seems name is a keyworkd and not loading proper data while looping with "iterrows" 
print('Not NUll values selected')
for_db_active_interested_assets_df = db_active_interested_assets_df.copy()
print('Dataframe copid')
for_db_active_interested_assets_df.rename(columns = {'name':'CName'},inplace = True)
print('name changed to CName')


print('Total Number of stocks to be scanned in this run')
print(for_db_active_interested_assets_df['CName'].count())


#Database connection String
db = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=localhost;Database=LuPapa;UID=azabhishek;PWD=Sunsh1ne@2;utocommit=True')
cursor = db.cursor()



#Loop to load the staging table [StagingAnalysis].[Alpaca_Active_Tickers_Stg] 
for index, row in for_db_active_interested_assets_df.iterrows():
    cursor.execute('insert into  [StagingAnalysis].[Alpaca_Active_Tickers_Stg] values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                                                                                                               row.symbol,
                                                                                                               row.CName, 
                                                                                                               row.id,
                                                                                                               row.status, 
                                                                                                               row.exchange, 
                                                                                                               row.easy_to_borrow,
                                                                                                               row.fractionable ,
                   
                                                                                                               row.marginable,
                                                                                                               row.shortable, 
                                                                                                               row.tradable,
                                                                                                               row.avg_30_day_volume, 
                                                                                                               row.avg_30_day_price, 
                                                                                                               row.last_eod_volume, 
                                                                                                               row.last_eod_price
                                                                                                            )
db.commit()


#Run the proc to load to the main table [Analysis].[Alpaca_Active_Tickers]
cursor.execute('exec [dbo].[AlpacaActiveTickersLoad]')                                                                                                     
db.commit()

#Close the database connection
db.close()

print('process completed ar '+ str(dtm.datetime.now()))