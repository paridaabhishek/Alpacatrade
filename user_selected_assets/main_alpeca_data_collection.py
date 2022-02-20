#####################Imort reqiired libreries##########################
from concurrent.futures import thread
import websocket
import json
from datetime import datetime
import pandas as pd
import numpy as np
import pytz
from datetime import datetime
from datetime import timedelta
import ssl
import threading


#######################import required functions#######################
from general import *
from paths import *

######################################################################


if __name__ == "__main__":
    try:

        print("testing Try")
        creds = get_credentails(cred_file)
        print(creds)
        stocks_in_interest = get_stocks(stock_file)
        print(stocks_in_interest)
        crypto_in_interest = get_crypto(crypto_file)
        print(crypto_in_interest)

        # print(stock_socket)
        # print(crypto_socket)
        ws_crypto = websocket.WebSocketApp(
            crypto_socket, on_open=on_ope_fun_crypto, on_message=on_msg_fun_crypto
        )

        ws_stock = websocket.WebSocketApp(
            stock_socket, on_open=on_ope_fun_stock, on_message=on_msg_fun_stock
        )
        # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        thread_stock = threading.Thread(target=ws_stock.run_forever())
        thread_crypto = threading.Thread(target=ws_crypto.run_forever())

        thread_stock.start()
        thread_crypto.start()

        thread_stock.join()
        thread_crypto.join()

        print("The data collection process ended !!!")

    except Exception as ex:
        print(str(ex))
