import ast
import json
from datetime import datetime
import datetime as dtm
import pandas as pd
from os import path
import os
import alpaca_trade_api as tradeapi
import pytz
from datetime import timedelta
import glob


#######################import required functions#######################
from paths import *
from transaction import *


def get_credentails(config_file):
    with open(config_file, "r") as credfile:
        return ast.literal_eval(credfile.read())


def get_stocks(stock_file):
    # print([line.strip() for line in open(stock_file, "r")])
    return [line.strip() for line in open(stock_file, "r")]


def get_crypto(crypto_file):
    # print([line.strip() for line in open(stock_file, "r")])
    return [line.strip() for line in open(crypto_file, "r")]


# print(get_stocks(stock_file))


def trading_window():
    creds = get_credentails(cred_file)
    api = tradeapi.REST(
        key_id=get_credentails(cred_file)["API_KEY"],
        secret_key=get_credentails(cred_file)["SECRET_KEY"],
        base_url=base_url,
    )

    caln = api.get_calendar(start=dtm.date.today(), end=dtm.date.today())
    date = caln[0].date
    open = caln[0].open
    close = caln[0].close
    s_close = caln[0].session_close
    s_open = caln[0].session_open

    # print(caln)
    # Normal Traing hors
    trading_start = dtm.datetime.combine(
        dtm.date(date.year, date.month, date.day), dtm.time(open.hour, open.minute)
    ) + dtm.timedelta(
        hours=-1
    )  # -1 to bring it to CST

    trading_end = dtm.datetime.combine(
        dtm.date(date.year, date.month, date.day), dtm.time(close.hour, close.minute)
    ) + dtm.timedelta(hours=-1)

    # Extended hour trading
    ext_trading_start = dtm.datetime.combine(
        dtm.date(date.year, date.month, date.day), dtm.time(s_open.hour, s_open.minute)
    ) + dtm.timedelta(hours=-1)
    ext_trading_end = dtm.datetime.combine(
        dtm.date(date.year, date.month, date.day),
        dtm.time(s_close.hour, s_close.minute),
    ) + dtm.timedelta(hours=-1)

    #####################At one point use one return
    # for normal tarding hours
    return dtm.datetime.now() > trading_start and dtm.datetime.now() < trading_end
    # for extedned trading hours
    # return (
    #     dtm.datetime.now() > ext_trading_start and dtm.datetime.now() < ext_trading_end
    # )


# print(trading_window())


def move_to_archive(stream_file, stream_archive_file):
    if path.exists(stream_file):
        os.rename(stream_file, stream_archive_file)
        print("Cstreaming file archived")
    else:
        print("Nothing to delere ")


def archive_staged_file(type):
    print(
        type + " --" + " Archiving Staged file as end of the process signal generated"
    )
    for name in glob.glob(staged_path + r"\\" + type + "*.csv"):

        # # + ".csv")
        # print(name)
        # print(
        #     staged_path_archive
        #     + name.split("staged")[1].split(".")[0]
        #     + "_"
        #     + str(time.strftime("%Y%m%d_%H_%M"))
        #     + ".csv"
        # )
        os.rename(
            name,
            staged_path_archive
            + name.split("staged")[1].split(".")[0]
            + "_"
            + str(time.strftime("%Y%m%d_%H_%M"))
            + ".csv",
        )


#####################Web Socket Functions###########################################
def on_ope_fun(ws):

    print("Opened")
    auth_data = {
        "action": "auth",
        "key": get_credentails(cred_file)["API_KEY"],
        "secret": get_credentails(cred_file)["SECRET_KEY"],
    }  # Key and Secret getting from the Cred file.
    print(auth_data)
    ws.send(json.dumps(auth_data))

    ###############Check if some entry in the stock file ################################
    ###And create the listen message for the stock to get the one min tickers############
    if os.stat(stock_file).st_size != 0:
        print(
            "Stock ----file has some ticker and non zero and will create the starter file"
        )
        with open(stock_starter_file, "w") as startfile:
            pass

        listen_message_stock = (
            '{"action":"subscribe","bars":'
            + str(get_stocks(stock_file)).replace("'", '"')
            + "}"
        )
        ws.send(json.dumps(json.loads(listen_message_stock)))
    # else:
    #     ws.close()

    ###############Check if some entry in the crypto file ################################
    ###And create the listen message for the stock to get the one min tickers############

    if os.stat(crypto_file).st_size != 0:
        print(
            "Crypto---- file has some ticker and non zero and will create the starter file"
        )
        with open(crypto_starter_file, "w") as startfile:
            pass

        listen_message_crypto = (
            '{"action":"subscribe","bars":'
            + str(get_crypto(crypto_file)).replace("'", '"')
            + "}"
        )
        ws.send(json.dumps(json.loads(listen_message_crypto)))
    # else:
    #     ws.close()


def on_msg_fun(ws, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if path.exists(stock_starter_file):
        print("Stock -- starter File exists:" + str(path.exists(stock_starter_file)))
        print("Stock messgae received at" + current_time)
        print(message)
        print("Stock --Strated wring to the steam file")
        print("Stock --Wrttin  steam file")
    else:
        print("stock ---Colosing the webscoket for stocks file deleted BYEE!!!!")
        ws.close()

    if path.exists(crypto_starter_file):
        print("Crypto --Starter File exists:" + str(path.exists(crypto_starter_file)))
        print("Crypto--messgae received at" + current_time)
        print(message)
        print("Crypto--Strated wring to the steam file")
        print("Crypto--Wrttin  steam file")
    else:
        print("Colosing the webscoket as the starter file deleted BYEE!!!!")
        ws.close()


#######################For Stock

#####################Web Socket Functions###########################################
def on_ope_fun_stock(ws):

    print("stock --Opened")
    auth_data = {
        "action": "auth",
        "key": get_credentails(cred_file)["API_KEY"],
        "secret": get_credentails(cred_file)["SECRET_KEY"],
    }  # Key and Secret getting from the Cred file.
    print("Stock--" + str(auth_data))
    ws.send(json.dumps(auth_data))

    ###############Check if some entry in the stock file ################################
    ###And create the listen message for the stock to get the one min tickers############
    if os.stat(stock_file).st_size != 0 and trading_window():
        print(
            "Stock ----file has some ticker and non zero and will create the starter file"
        )
        with open(stock_starter_file, "w") as startfile:
            pass

        listen_message_stock = (
            '{"action":"subscribe","bars":'
            + str(get_stocks(stock_file)).replace("'", '"')
            + "}"
        )
        ws.send(json.dumps(json.loads(listen_message_stock)))
    else:
        print("stock ---Stock file is empty or outside trading window")
        # ws.close()


def on_msg_fun_stock(ws, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if path.exists(stock_starter_file):
        print("Stock -- starter File exists:" + str(path.exists(stock_starter_file)))
        print("Stock messgae received at" + current_time)
        print(message)
        print("Stock --Strated wring to the steam file")

        if "error" in message:
            print("Stock--ERRORRR-->" + str(message))
            print("Stock--Removing teh starter file")
            os.remove(stock_starter_file)
            ws.close()
        else:
            stream_stock(message)  ## Stream the websocket to the data file.
            print("Stock --Wrttin  steam file")
            staged_stock()
            print("Stock --Staged")

    else:
        print("Stock ---Colosing the webscoket for stocks file deleted BYEE!!!!")
        ws.close()
        print("Stock---Moving the stream file to the backup location with time stamp")
        move_to_archive(stock_stream_file, stock_stream_archive_file)
        archive_staged_file("Stock")


# OnetoFiveMinLive(message)


def stream_stock(message):
    # print("Streaming Crypto")
    # messageJson = json.loads(message)
    # df_crypto = pd.DataFrame(messageJson)
    print("stock--Printing dataframe")
    # print(df)
    if not (path.exists(stock_stream_file)):
        print("Stock ---stockstream.csv will be crated as it does not exits!!")
        columns = [
            "Message Type",
            "Symbol",
            "Open",
            "Close",
            "High",
            "Low",
            "Volume",
            "TimeStamp",
            "n",
            "vw",
        ]

        df_stock_empty = pd.DataFrame(columns=columns)
        print(df_stock_empty)
        df_stock_empty.to_csv(stock_stream_file, index=False, header=True)

    else:
        messageJson = json.loads(message)
        df_stock = pd.DataFrame(messageJson)
        print("=============================")
        print(df_stock[df_stock["T"] == "b"])
        print("=============================")
        df_stock[df_stock["T"] == "b"].to_csv(
            stock_stream_file, mode="a", index=False, header=False
        )

        # read the stream file . Then get the last 1313 records and rewrite to the same CSV.
        # this is to make sure the file conntains the latest 1313 recors.
        pd.read_csv(stock_stream_file, index_col=None).iloc[-1313:].to_csv(
            stock_stream_file, index=False, header=True
        )


# as and when new business logic arrives ,the source data colums will be added here
# this prossed data will be used to carry out transactions latter to generate the profit
# v1
def staged_stock():
    print("Stock-- This is to generate the 1,5,15 mins signals")
    streamd_df = pd.read_csv(stock_stream_file, index_col=False)
    # streamd_df_cbse = streamd_df[]

    # this is to convert the time zone to cntral UAS . Based on the location the time zone can be adjusted
    # for the proper understanding of the data . Without this the time zone is UTC as per alpeca.
    eastern = pytz.timezone("US/Central")

    # for all the cryptos interested carry out teh loop and extract the
    # 1 5 and 15 mins signals . This can be more dynamic in future which can also contaion other timeframes.
    for ticker in streamd_df["Symbol"].unique():
        # print(ticker)
        # print(type(str(ticker)))
        # # print(
        # #     streamd_df_cbse[streamd_df_cbse["Symbol"] == ticker]
        # #     .drop_duplicates(subset=["TimeStamp"])
        # #     .copy()
        # # )

        # sometime the socket sending multiple streams for
        streamd_df_unique = (
            streamd_df[streamd_df["Symbol"] == ticker]
            .drop_duplicates(subset=["TimeStamp"])
            .copy()
        )

        # convert the Timestamp field to datetime
        streamd_df_unique.loc[:, "TimeStamp"] = pd.to_datetime(
            streamd_df_unique["TimeStamp"]
        )
        streamd_df_unique.set_index("TimeStamp", inplace=True)

        # print("Before timezone shift")
        # print(streamd_df_cbse_unique)
        streamd_df_unique.index = streamd_df_unique.index.tz_convert(eastern)
        # print("After timezone shift")
        # print(streamd_df_cbse_unique)

        streamd_df_unique["5MinReminder"] = streamd_df_unique.index.minute % 5
        streamd_df_unique["15MinReminder"] = (
            streamd_df_unique.index.minute % 15
        )  # incase want to code for 15 mins bars

        # print("---With Reminders ------------------")
        # print(streamd_df_cbse_unique)

        ######----->1 mins signal creation block started ###############################
        streamed_df_1mins_bar = streamd_df_unique.copy()

        streamed_df_1mins_bar["9EMAClosed"] = (
            streamed_df_1mins_bar["Close"].ewm(span=9, adjust=True).mean()
        )

        streamed_df_1mins_bar["21EMAClosed"] = (
            streamed_df_1mins_bar["Close"].ewm(span=21, adjust=True).mean()
        )

        streamed_df_1mins_bar.to_csv(
            staged_path + r"/" + "Stock_" + ticker + "_1Min.csv",
            index=True,
            header=True,
        )

        # print("---------1mins dataframe-------->>>")
        # # print(streamd_df_cbse_unique_1min)
        # print(streamed_df_1mins_bar)

        ######<-----1 mins signal creation block ended #################################

        ######----->5 mins signal creation block started ###############################
        # #gets min time time where the 5 mins remider is zero.
        start_time_5mins = streamd_df_unique[
            streamd_df_unique["5MinReminder"] == 0
        ].index.min() + timedelta(minutes=0)

        end_time_5mins = streamd_df_unique[
            streamd_df_unique["5MinReminder"] == 4
        ].index.max() + timedelta(minutes=0)

        print("Start time 5 mins -:" + str(start_time_5mins))
        print("Start time 5 mins -:" + str(end_time_5mins))

        streamd_df_unique_5min = streamd_df_unique.loc[
            start_time_5mins:end_time_5mins
        ].copy()

        streamed_df_5mins_bar = (
            streamd_df_unique_5min.groupby(pd.Grouper(freq="5min")).agg(
                {"Open": "first", "Close": "last", "High": "max", "Low": "min"}
            )
            ##.iloc[1:]
        )

        streamed_df_5mins_bar["Symbol"] = ticker

        streamed_df_5mins_bar["9EMAClosed"] = (
            streamed_df_5mins_bar["Close"].ewm(span=9, adjust=True).mean()
        )
        streamed_df_5mins_bar["21EMAClosed"] = (
            streamed_df_5mins_bar["Close"].ewm(span=21, adjust=True).mean()
        )

        streamed_df_5mins_bar.to_csv(
            staged_path + r"/" + "Stock_" + ticker + "_5Min.csv",
            index=True,
            header=True,
        )

        # print("---------5mins dataframe-------->>>")
        # print(streamd_df_cbse_unique_5min)
        # print(
        #     streamed_df_5mins_bar[
        #         ["Symbol", "Open", "Close", "High", "Low", "9EMAClosed", "21EMAClosed"]
        #     ]
        # )
        #######5 mins signal creation block ended<---------------- #################

        ######----->15 mins signal creation block started ###############################
        # first pointer from where the 5 mins bar will start for now 0 mims addition is giving proper result . Need to be checkd further.
        start_time_15mins = streamd_df_unique[
            streamd_df_unique["15MinReminder"] == 0
        ].index.min() + timedelta(
            minutes=0
        )  # first pointer from where the 15 mins bar will start.The timedelta is just a 0 min addition and need to be tested further.

        end_time_15mins = streamd_df_unique[
            streamd_df_unique["15MinReminder"] == 14
        ].index.max() + timedelta(minutes=0)

        # print("Start time 15 mins -:" + str(start_time_15mins))

        streamd_df_unique_15min = streamd_df_unique.loc[start_time_15mins:].copy()

        streamed_df_15mins_bar = (
            streamd_df_unique_15min.groupby(pd.Grouper(freq="15min")).agg(
                {"Open": "first", "Close": "last", "High": "max", "Low": "min"}
            )
            ##.iloc[1:]
        )

        streamed_df_15mins_bar["Symbol"] = ticker

        streamed_df_15mins_bar["9EMAClosed"] = (
            streamed_df_15mins_bar["Close"].ewm(span=9, adjust=True).mean()
        )

        streamed_df_15mins_bar["21EMAClosed"] = (
            streamed_df_15mins_bar["Close"].ewm(span=21, adjust=True).mean()
        )

        streamed_df_15mins_bar.to_csv(
            staged_path + r"/" + "Stock_" + ticker + "_15Min.csv",
            index=True,
            header=True,
        )

        # print("---------15mins dataframe-------->>>")
        # print(streamd_df_cbse_unique_15min)
        # print(
        #     streamed_df_15mins_bar[
        #         ["Symbol", "Open", "Close", "High", "Low", "9EMAClosed", "21EMAClosed"]
        #     ]
        # )

        # print("---------15mins dataframe-------->>>")
        # print(streamd_df_cbse_unique_15min)

    ######----->15 mins signal creation block ended ###############################


#######################For Crypto

#####################Web Socket Functions###########################################
def on_ope_fun_crypto(ws):

    print("Crypto--Opened")
    auth_data = {
        "action": "auth",
        "key": get_credentails(cred_file)["API_KEY"],
        "secret": get_credentails(cred_file)["SECRET_KEY"],
    }  # Key and Secret getting from the Cred file.
    print("Crypto --" + str(auth_data))
    ws.send(json.dumps(auth_data))

    ###############Check if some entry in the stock file ################################
    ###And create the listen message for the stock to get the one min tickers############
    if os.stat(crypto_file).st_size != 0:
        print(
            "Crypto ----file has some ticker and non zero and will create the starter file"
        )
        with open(crypto_starter_file, "w") as startfile:
            pass

        listen_message_crypto = (
            '{"action":"subscribe","bars":'
            + str(get_crypto(crypto_file)).replace("'", '"')
            + "}"
        )
        ws.send(json.dumps(json.loads(listen_message_crypto)))
    else:
        print("Crypto --- Crypto file is empty")


def on_msg_fun_crypto(ws, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if path.exists(crypto_starter_file):
        print("Crypto -- starter File exists:" + str(path.exists(crypto_starter_file)))
        print("Crypto messgae received at" + current_time)
        print(message)
        print("Crypto --Strated wring to the steam file")

        if "error" in message:
            print("Crypto--ERRORRR-->" + str(message))
            print("Crypto--Removing teh starter file")
            os.remove(crypto_starter_file)
            ws.close()
        else:
            stream_crypto(message)  ## Stream the websocket to the data file.
            staged_crypto()
            trans_5Min_921EMA_crypto()

        print("Crypto --Wrttin  steam file")
    else:
        print("Crypto ---Colosing the webscoket for Crypto file deleted BYEE!!!!")
        ws.close()
        print("Crypto--Moving the stream file to the backup location with time stamp")
        move_to_archive(crypto_stream_file, crypto_stream_archive_file)
        archive_staged_file("Crypto")


def stream_crypto(message):
    # print("Streaming Crypto")
    # messageJson = json.loads(message)
    # df_crypto = pd.DataFrame(messageJson)
    print("Printing dataframe")
    # print(df)
    if not (path.exists(crypto_stream_file)):
        print("Crypro ---cryptostream.csv will be crated as it does not exits!!")
        columns = [
            "Message Type",
            "Symbol",
            "Exchange",
            "Open",
            "Close",
            "High",
            "Low",
            "Volume",
            "TimeStamp",
            "n",
            "vw",
        ]
        df_crypto_empty = pd.DataFrame(columns=columns)
        print(df_crypto_empty)
        df_crypto_empty.to_csv(crypto_stream_file, index=False, header=True)

    else:
        messageJson = json.loads(message)
        df_crypto = pd.DataFrame(messageJson)
        print("=============================")
        print(df_crypto[df_crypto["T"] == "b"])
        print("=============================")
        df_crypto[df_crypto["T"] == "b"].to_csv(
            crypto_stream_file, mode="a", index=False, header=False
        )

        # read the stream file . Then get the last 1313 records and rewrite to the same CSV.
        # this is to make sure the file conntains the latest 1313 recors.
        pd.read_csv(crypto_stream_file, index_col=None).iloc[-1313:].to_csv(
            crypto_stream_file, index=False, header=True
        )


# as and when new business logic arrives ,the source data colums will be added here
# this prossed data will be used to carry out transactions latter to generate the profit
# v1
def staged_crypto():
    print("Crypto-- This is to generate the 1,5,15 mins signals")
    streamd_df = pd.read_csv(crypto_stream_file, index_col=False)
    # streamd_df_cbse = streamd_df[]

    # for crypto only taking the coinbase exchange as its the largest for now and can be more accurate
    streamd_df_cbse = streamd_df[streamd_df["Exchange"] == "CBSE"]
    # print(streamd_df[streamd_df["Exchange"] == "CBSE"])
    # print(type(streamd_df_cbse["Symbol"].unique()))

    # this is to convert the time zone to cntral UAS . Based on the location the time zone can be adjusted
    # for the proper understanding of the data . Without this the time zone is UTC as per alpeca.
    eastern = pytz.timezone("US/Central")

    # for all the cryptos interested carry out teh loop and extract the
    # 1 5 and 15 mins signals . This can be more dynamic in future which can also contaion other timeframes.
    for ticker in streamd_df_cbse["Symbol"].unique():
        # print(ticker)
        # print(type(str(ticker)))
        # # print(
        # #     streamd_df_cbse[streamd_df_cbse["Symbol"] == ticker]
        # #     .drop_duplicates(subset=["TimeStamp"])
        # #     .copy()
        # # )

        #
        streamd_df_cbse_unique = (
            streamd_df_cbse[streamd_df_cbse["Symbol"] == ticker]
            .drop_duplicates(subset=["TimeStamp"])
            .copy()
        )

        streamd_df_cbse_unique.loc[:, "TimeStamp"] = pd.to_datetime(
            streamd_df_cbse_unique["TimeStamp"]
        )
        streamd_df_cbse_unique.set_index("TimeStamp", inplace=True)

        # print("Before timezone shift")
        # print(streamd_df_cbse_unique)
        streamd_df_cbse_unique.index = streamd_df_cbse_unique.index.tz_convert(eastern)
        # print("After timezone shift")
        # print(streamd_df_cbse_unique)

        streamd_df_cbse_unique["5MinReminder"] = streamd_df_cbse_unique.index.minute % 5
        streamd_df_cbse_unique["15MinReminder"] = (
            streamd_df_cbse_unique.index.minute % 15
        )  # incase want to code for 15 mins bars

        # print("---With Reminders ------------------")
        # print(streamd_df_cbse_unique)

        ######----->1 mins signal creation block started ###############################
        streamed_df_1mins_bar = streamd_df_cbse_unique.copy()

        streamed_df_1mins_bar["9EMAClosed"] = (
            streamed_df_1mins_bar["Close"].ewm(span=9, adjust=True).mean()
        )

        streamed_df_1mins_bar["21EMAClosed"] = (
            streamed_df_1mins_bar["Close"].ewm(span=21, adjust=True).mean()
        )

        streamed_df_1mins_bar.to_csv(
            staged_path + r"/" + "Crypto_" + ticker + "_1Min.csv",
            index=True,
            header=True,
        )

        # print("---------1mins dataframe-------->>>")
        # # print(streamd_df_cbse_unique_1min)
        # print(streamed_df_1mins_bar)

        ######<-----1 mins signal creation block ended #################################

        ######----->5 mins signal creation block started ###############################
        # #gets min time time where the 5 mins remider is zero.
        start_time_5mins = streamd_df_cbse_unique[
            streamd_df_cbse_unique["5MinReminder"] == 0
        ].index.min() + timedelta(minutes=0)

        end_time_5mins = streamd_df_cbse_unique[
            streamd_df_cbse_unique["5MinReminder"] == 4
        ].index.max() + timedelta(minutes=0)

        print("Start time 5 mins -:" + str(start_time_5mins))
        print("End time 5 mins -:" + str(start_time_5mins))

        streamd_df_cbse_unique_5min = streamd_df_cbse_unique.loc[
            start_time_5mins:end_time_5mins
        ].copy()

        streamed_df_5mins_bar = (
            streamd_df_cbse_unique_5min.groupby(pd.Grouper(freq="5min")).agg(
                {"Open": "first", "Close": "last", "High": "max", "Low": "min"}
            )
            ##.iloc[1:]
        )

        streamed_df_5mins_bar["Symbol"] = ticker

        streamed_df_5mins_bar["9EMAClosed"] = (
            streamed_df_5mins_bar["Close"].ewm(span=9, adjust=True).mean()
        )
        streamed_df_5mins_bar["21EMAClosed"] = (
            streamed_df_5mins_bar["Close"].ewm(span=21, adjust=True).mean()
        )

        streamed_df_5mins_bar.to_csv(
            staged_path + r"/" + "Crypto_" + ticker + "_5Min.csv",
            index=True,
            header=True,
        )

        # print("---------5mins dataframe-------->>>")
        # print(streamd_df_cbse_unique_5min)
        # print(
        #     streamed_df_5mins_bar[
        #         ["Symbol", "Open", "Close", "High", "Low", "9EMAClosed", "21EMAClosed"]
        #     ]
        # )
        #######5 mins signal creation block ended<---------------- #################

        ######----->15 mins signal creation block started ###############################
        # first pointer from where the 5 mins bar will start for now 0 mims addition is giving proper result . Need to be checkd further.
        start_time_15mins = streamd_df_cbse_unique[
            streamd_df_cbse_unique["15MinReminder"] == 0
        ].index.min() + timedelta(
            minutes=0
        )  # first pointer from where the 15 mins bar will start.The timedelta is just a 0 min addition and need to be tested further.

        end_time_15mins = streamd_df_cbse_unique[
            streamd_df_cbse_unique["15MinReminder"] == 14
        ].index.max() + timedelta(minutes=0)

        # print("Start time 15 mins -:" + str(start_time_15mins))

        streamd_df_cbse_unique_15min = streamd_df_cbse_unique.loc[
            start_time_15mins:end_time_15mins
        ].copy()

        streamed_df_15mins_bar = (
            streamd_df_cbse_unique_15min.groupby(pd.Grouper(freq="15min")).agg(
                {"Open": "first", "Close": "last", "High": "max", "Low": "min"}
            )
            ##.iloc[1:]
        )

        streamed_df_15mins_bar["Symbol"] = ticker

        streamed_df_15mins_bar["9EMAClosed"] = (
            streamed_df_15mins_bar["Close"].ewm(span=9, adjust=True).mean()
        )

        streamed_df_15mins_bar["21EMAClosed"] = (
            streamed_df_15mins_bar["Close"].ewm(span=21, adjust=True).mean()
        )

        streamed_df_15mins_bar.to_csv(
            staged_path + r"/" + "Crypto_" + ticker + "_15Min.csv",
            index=True,
            header=True,
        )

        # print("---------15mins dataframe-------->>>")
        # print(streamd_df_cbse_unique_15min)
        # print(
        #     streamed_df_15mins_bar[
        #         ["Symbol", "Open", "Close", "High", "Low", "9EMAClosed", "21EMAClosed"]
        #     ]
        # )

        # print("---------15mins dataframe-------->>>")
        # print(streamd_df_cbse_unique_15min)

    ######----->15 mins signal creation block ended ###############################
