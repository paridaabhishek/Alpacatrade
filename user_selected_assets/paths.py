import time


#################This need to be modified#######################
base_bath = r"C:\Users\abhis\DATA\Alpeca"
base_url = "https://paper-api.alpaca.markets"  # Chnage it to live for real trading


#################This will remain constant###########################
cred_file = base_bath + r"\config\cred.txt"
stock_file = base_bath + r"\config\stocks.txt"
crypto_file = base_bath + r"\config\crypto.txt"

stock_starter_file = base_bath + r"\starter\stock.start"
crypto_starter_file = base_bath + r"\starter\crypto.start"

crypto_stream_file = base_bath + r"\stream\cryptostream.csv"
stock_stream_file = base_bath + r"\stream\stockstream.csv"


crypto_stream_archive_file = (
    base_bath
    + r"\stream\Archive\cryptostream_"
    + str(time.strftime("%Y%m%d_%H_%M"))
    + ".csv"
)

stock_stream_archive_file = (
    base_bath
    + r"\stream\Archive\stockstream_"
    + str(time.strftime("%Y%m%d_%H_%M"))
    + ".csv"
)


stock_socket = "wss://stream.data.alpaca.markets/v2/sip"
crypto_socket = "wss://stream.data.alpaca.markets/v1beta1/crypto"
