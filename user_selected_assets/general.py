import ast
import json
from datetime import datetime
from os import path
import os


#######################import required functions#######################
from paths import *


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
    else:
        print("stock ---Stock file is empty")
        # ws.close()


def on_msg_fun_stock(ws, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if path.exists(stock_starter_file):
        print("Stock -- starter File exists:" + str(path.exists(stock_starter_file)))
        print("Stock messgae received at" + current_time)
        print(message)
        print("Stock --Strated wring to the steam file")
        print("Stock --Wrttin  steam file")
    else:
        print("Stock ---Colosing the webscoket for stocks file deleted BYEE!!!!")
        ws.close()


# OnetoFiveMinLive(message)


#######################For Crypto

#####################Web Socket Functions###########################################
def on_ope_fun_crypto(ws):

    print("Crypto--Opened")
    auth_data = {
        "action": "auth",
        "key": get_credentails(cred_file)["API_KEY"],
        "secret": get_credentails(cred_file)["SECRET_KEY"],
    }  # Key and Secret getting from the Cred file.
    print(auth_data)
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
        print("Crypto --Wrttin  steam file")
    else:
        print("Crypto ---Colosing the webscoket for stocks file deleted BYEE!!!!")
        ws.close()
