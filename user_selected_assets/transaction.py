from paths import *
import numpy as np
import json
import glob
from os import path
import pandas as pd
import ast
import alpaca_trade_api as tradeapi
import os


##get the connection for transaction use
def get_account_connection_api():
    with open(cred_file, "r") as credfile:
        # print(ast.literal_eval(credfile.read()))
        creds = ast.literal_eval(credfile.read())

    print(creds["API_KEY"])
    print(creds["SECRET_KEY"])

    conn = tradeapi.REST(
        key_id=creds["API_KEY"],
        secret_key=creds["SECRET_KEY"],
        base_url=base_url,
    )

    return conn


def crypto_buy(ticker, quantity):
    print("Buying with crypto buying function  ")
    conn = get_account_connection_api()
    r = conn.submit_order(symbol=ticker, qty=quantity, side="buy", type="market")
    return r


def crypto_sell(ticker):
    print("Selling the crypto with selling function  ")
    conn = get_account_connection_api()
    c = conn.close_position(ticker)
    return c


def stock_buy(ticker, quantity):
    print("Buying with Stock buying function  ")
    conn = get_account_connection_api()
    r = conn.submit_order(symbol=ticker, qty=quantity, side="buy", type="market")
    return r


def stock_sell(ticker):
    print("Selling the Stock with selling function  ")
    conn = get_account_connection_api()
    c = conn.close_position(ticker)
    return c


def if_positions_exists(ticker):
    conn = get_account_connection_api()
    print([s.symbol for s in conn.list_positions()])

    if ticker in [s.symbol for s in conn.list_positions()]:
        return True
    else:
        return False


def archive_trans_file(type):
    print(type + " --" + " Archiving trans file as end of the process signal generated")
    for name in glob.glob(tarns_path + r"\\" + type + "*.csv"):

        # # + ".csv")
        print(name)
        print(name.split(".")[0] + "_" + str(time.strftime("%Y%m%d_%H_%M")) + ".csv")
        print(tarns_path_archived)
        # print(
        #     tarns_path_archived
        #     + name.split("staged")[1].split(".")[0]
        #     + "_"
        #     + str(time.strftime("%Y%m%d_%H_%M"))
        #     + ".csv"
        # )
        os.rename(
            name,
            tarns_path_archived
            + name.split("trans")[1].split(".")[0]
            + "_"
            + str(time.strftime("%Y%m%d_%H_%M"))
            + ".csv",
        )


def log_transaction(ticker):
    print("Selling the crypto with selling function  ")
    conn = get_account_connection_api()
    ticker_lst = []
    ticker_lst.append(ticker)
    orders = conn.list_orders(ticker_lst, limit=500)
    # print(orders)

    orders_df = pd.DataFrame(
        {
            "symbol": [x.symbol for x in orders],
            "side": [x.side for x in orders],
            "qty": [x.qty for x in orders],
            "filled_avg_price": [x.filled_avg_price for x in orders],
            "filled_qty": [x.filled_qty for x in orders],
            # "AssetTransacted": [
            #     (float(x.filled_qty) * float(x.filled_avg_price)) for x in orders
            # ],
            "asset_class": [x.asset_class for x in orders],
            "id": [x.id for x in orders],
            "asset_id": [x.asset_id for x in orders],
            "client_order_id": [x.client_order_id for x in orders],
            "created_at": [x.created_at for x in orders],
            "filled_at": [x.filled_at for x in orders],
            "submitted_at": [x.submitted_at for x in orders],
            "updated_at": [x.updated_at for x in orders],
        }
    )

    orders_df = orders_df[orders_df["symbol"] == ticker]
    orders_df["AssetTransacted"] = orders_df["filled_qty"].astype(float) * orders_df[
        "filled_avg_price"
    ].astype(float)

    orders_df[
        [
            "symbol",
            "side",
            "qty",
            "filled_qty",
            "filled_avg_price",
            "AssetTransacted",
            "asset_class",
            "id",
            "asset_id",
            "client_order_id",
            "created_at",
            "filled_at",
            "submitted_at",
            "updated_at",
        ]
    ].to_csv(tarns_path + r"/Crypto_" + ticker + "_transaction_details.csv", index=None)


def set_assets():

    with open(stock_file) as file:
        stocks = [line.rstrip() for line in file]
    with open(crypto_file) as file:
        cryptos = [line.rstrip() for line in file]

    equity_pct = []

    if (len(stocks) + len(cryptos)) != 0:
        total_asset = int(input("Enter the total asset you want to trade :"))
        print(
            "The Algo will trade :"
            + str(stocks + cryptos)
            + "  as per your input .Giev a Persentage  allocation to each with total persentage is 100 "
        )

        equity_pct = []

        for equity in stocks + cryptos:

            pct = float(input("Enter persentage of " + equity + " you want to put :"))
            equity_pct.append(pct)

        if total_asset > 10 and sum(equity_pct) == 100:

            trans_details = dict(
                list(zip(stocks + cryptos, (total_asset * np.array(equity_pct)) / 100))
            )
            print(
                dict(
                    list(
                        zip(
                            stocks + cryptos, (total_asset * np.array(equity_pct)) / 100
                        )
                    )
                )
            )

            print(
                "Congrats!!!All criteria maching trasactions will be carried out with signals"
            )

            with open(asset_file, "w") as transfile:
                transfile.write(str(total_asset) + "\n")
                transfile.write(str(trans_details))

            with open(trans_starter_file, "w") as startfile:
                pass

        else:
            print(
                "Even if tickers are present either the total asset is less than 11 or total persentage is not comming 100!!!"
            )
            print(
                ".. No transaction will happen though the signals will be generated !!!"
            )

    else:
        print("Not Enough tickers to start the trasaction!!!!")


# set_assets()


def trans_5Min_921EMA_crypto():

    if path.exists(trans_starter_file):
        print(
            "The trans starter file exits and ..Trans for 5Min 921EMA started for crypto"
        )

        with open(crypto_file, "r") as cryptof:
            crypto_tickers = [line.rstrip() for line in cryptof]
            print(crypto_tickers)

        with open(asset_file, "r") as transstart:
            asset_info = [line.rstrip() for line in transstart]
            print(asset_info[0])

        asset_alloc_details = json.loads(str(asset_info[1]).replace("'", '"'))
        for key in asset_alloc_details:
            if key in crypto_tickers:
                print(key, str(asset_alloc_details[key]))
                ticker = key
                alloc_amount = asset_alloc_details[key]
                for name in glob.glob(staged_path + r"\\*" + key + "_5Min*.csv"):
                    print(name)
                    name_1Min = name.replace("_5Min", "_1Min")
                    print(name_1Min)

                    df_staged_5Min = pd.read_csv(name, index_col="TimeStamp")
                    df_staged_5Min.index = pd.to_datetime(df_staged_5Min.index)

                    # df_staged_1Min = pd.read_csv(name_1Min, index_col="TimeStamp")
                    # df_staged_1Min.index = pd.to_datetime(name_1Min.index)

                    quantity = alloc_amount / df_staged_5Min.iloc[-1]["Close"]
                    print("Quantity in interest :" + str(quantity))
                    # print(type(df_staged_5Min.index))
                    if len(df_staged_5Min.index) > 3:
                        print("Crypto-- Enough datapoint to check for the transaction ")
                        if (
                            (
                                df_staged_5Min.iloc[-1]["9EMAClosed"]
                                > df_staged_5Min.iloc[-1]["21EMAClosed"]
                            )
                            and (
                                df_staged_5Min.iloc[-2]["9EMAClosed"]
                                <= df_staged_5Min.iloc[-2]["21EMAClosed"]
                            )
                            and not if_positions_exists(ticker)
                        ):

                            print(
                                "Buy and get the buying price and store it in a file"
                            )  # buying while the trend changed from 1 -ve to 2 +ve

                            status = crypto_buy(ticker, quantity)
                            # print(status)
                            log_transaction(ticker)

                            # write the trasns info to the file:
                            # with open(
                            #     tarns_path + r"/Crypto_" + ticker + "_buy_detail.txt",
                            #     "a",
                            # ) as buyfile:
                            #     buyfile.write(str(status).split("(")[1].split(")")[0])
                            #     buyfile.write("\n")

                        elif (
                            (
                                df_staged_5Min.iloc[-2]["9EMAClosed"]
                                >= df_staged_5Min.iloc[-2]["21EMAClosed"]
                            )
                            and (
                                df_staged_5Min.iloc[-1]["21EMAClosed"]
                                >= df_staged_5Min.iloc[-1]["9EMAClosed"]
                            )
                            and if_positions_exists(ticker)
                        ):  # if you have the asset and if you are getting .5% profit sell if 9<21 sell or stop transaction on 1 min bars
                            print(key)
                            print("Seling------------------------>>>")
                            sell = crypto_sell(ticker)
                            # print(sell)
                            log_transaction(ticker)
                        else:
                            print("Doing nothing and just wating for the next signal")

    else:
        print("Archiving Trans as trans starter is closed")
        archive_trans_file("Crypto")


def trans_5Min_921EMA_stock():

    if path.exists(trans_starter_file):
        print(
            "Stock:The trans starter file exits and ..Trans for 5Min 921EMA started for stock"
        )

        with open(stock_file, "r") as stockf:
            stock_tickers = [line.rstrip() for line in stockf]
            print(stock_tickers)

        with open(asset_file, "r") as transstart:
            asset_info = [line.rstrip() for line in transstart]
            print(asset_info[0])

        asset_alloc_details = json.loads(str(asset_info[1]).replace("'", '"'))
        for key in asset_alloc_details:
            if key in stock_tickers:
                print(key, str(asset_alloc_details[key]))
                ticker = key
                alloc_amount = asset_alloc_details[key]
                for name in glob.glob(staged_path + r"\\*" + key + "_5Min*.csv"):
                    print(name)
                    name_1Min = name.replace("_5Min", "_1Min")
                    print(name_1Min)

                    df_staged_5Min = pd.read_csv(name, index_col="TimeStamp")
                    df_staged_5Min.index = pd.to_datetime(df_staged_5Min.index)

                    # df_staged_1Min = pd.read_csv(name_1Min, index_col="TimeStamp")
                    # df_staged_1Min.index = pd.to_datetime(name_1Min.index)

                    quantity = alloc_amount / df_staged_5Min.iloc[-1]["Close"]
                    print("Stock :Quantity in interest :" + str(quantity))
                    # print(type(df_staged_5Min.index))
                    if len(df_staged_5Min.index) > 3:
                        print("Stock-- Enough datapoint to check for the transaction ")
                        if (
                            (
                                df_staged_5Min.iloc[-1]["9EMAClosed"]
                                > df_staged_5Min.iloc[-1]["21EMAClosed"]
                            )
                            and (
                                df_staged_5Min.iloc[-2]["9EMAClosed"]
                                < df_staged_5Min.iloc[-2]["21EMAClosed"]
                            )
                            and not if_positions_exists(ticker)
                        ):

                            print(
                                "Stock :Buy and get the buying price and store it in a file"
                            )  # buying while the trend changed from 1 -ve to 2 +ve

                            status = stock_buy(ticker, quantity)
                            print(status)
                            log_transaction(ticker)

                            # write the trasns info to the file:
                            with open(
                                tarns_path + r"/Stock_" + ticker + "_buy_detail.txt",
                                "a",
                            ) as buyfile:
                                buyfile.write(str(status).split("(")[1].split(")")[0])
                                buyfile.write("\n")

                        elif (
                            (
                                df_staged_5Min.iloc[-2]["9EMAClosed"]
                                >= df_staged_5Min.iloc[-2]["21EMAClosed"]
                            )
                            and (
                                df_staged_5Min.iloc[-1]["21EMAClosed"]
                                >= df_staged_5Min.iloc[-1]["9EMAClosed"]
                            )
                            and if_positions_exists(ticker)
                        ):  # if you have the asset and if you are getting .5% profit sell if 9<21 sell or stop transaction on 1 min bars
                            print(key)
                            print("Stock:Seling------------------------>>>")
                            sell = stock_sell(ticker)
                            print(sell)

                            log_transaction(ticker)

                        else:
                            print(
                                "Stock :Doing nothing and just wating for the next signal"
                            )
    else:

        archive_trans_file("Stock")
