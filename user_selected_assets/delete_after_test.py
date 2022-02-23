import ast
from email import header
import json
from datetime import datetime
from operator import index
from os import path
import os
from wave import Wave_write
import pandas as pd
from paths import *
import pytz
from datetime import datetime
from datetime import timedelta
import pandas as pd

#######################import required functions#######################


# def get_stocks(stock_file):
#     # print([line.strip() for line in open(stock_file, "r")])
#     return [line.strip() for line in open(stock_file, "r")]


# print(get_stocks(r"C:\Users\abhis\DATA\Alpeca\config\stocksBkp.txt"))


# print(os.stat(stock_file).st_size)

# df = pd.read_csv(
#     r"C:\Users\abhis\DATA\Alpeca\stream\Archive\cryptostream_20220221_10_17.csv",
#     index_col=None,
# )
# print(df)

# df = df.iloc[-1:]

# print(df)

# df.to_csv(
#     r"C:\Users\abhis\DATA\Alpeca\stream\Archive\cryptostream_20220221_10_17.csv",
#     index=False,
#     header=True,
# )


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
            staged_path + r"/" + ticker + "1Min.csv", index=True, header=True
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

        print("Start time 5 mins -:" + str(start_time_5mins))

        streamd_df_cbse_unique_5min = streamd_df_cbse_unique.loc[
            start_time_5mins:
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
            staged_path + r"/" + ticker + "5Min.csv", index=True, header=True
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

        # print("Start time 15 mins -:" + str(start_time_15mins))

        streamd_df_cbse_unique_15min = streamd_df_cbse_unique.loc[
            start_time_15mins:
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
            staged_path + r"/" + ticker + "15Min.csv", index=True, header=True
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


# import glob
# glob.glob('C:\Users\abhis\DATA\Alpeca\staged\.csv')

import glob

staged_path = base_bath + r"\staged"
staged_path_archive = base_bath + r"\staged\Archive"

# # # def archive_staged_files
# for name in glob.glob(staged_path + r"\Crypto*.csv"):
# for name in glob.glob(staged_path + r"\\" + "Crypto" + "*.csv"):

#     print(name)
# #     print(
#         staged_path_archive
#         + name.split("staged")[1].split(".")[0]
#         + "_"
#         + str(time.strftime("%Y%m%d_%H_%M"))
#         + ".csv"
#     )
# os.rename(
#     name,
#     staged_path_archive
#     + name.split("staged")[1].split(".")[0]
#     + "_"
#     + str(time.strftime("%Y%m%d_%H_%M"))
#     + ".csv",
# )

print(staged_path + r"\Crypto" + "*.csv")
print(staged_path + r"\Crypto*.csv")


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


archive_staged_file("Crypto")


# crypto_stream_archive_file = (
#     base_bath
#     + r"\stream\Archive\cryptostream_"
#     + str(time.strftime("%Y%m%d_%H_%M"))
#     + ".csv"
# )

# stock_stream_archive_file = (
#     base_bath
#     + r"\stream\Archive\stockstream_"
#     + str(time.strftime("%Y%m%d_%H_%M"))
#     + ".csv"
# )


#     def move_to_archive(stream_file, stream_archive_file):
#     if path.exists(stream_file):
#         os.rename(stream_file, stream_archive_file)
#         print("Cstreaming file archived")
#     else:
#         print("Nothing to delere ")
