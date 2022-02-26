import time


#################This need to be modified#######################
base_bath = r"C:\Users\abhis\DATA\Alpeca"
base_url = "https://paper-api.alpaca.markets"  # Chnage it to live for real trading


#################This will remain constant###########################
cred_file = base_bath + r"\config\cred.txt"
stock_file = base_bath + r"\config\stocks.txt"
crypto_file = base_bath + r"\config\crypto.txt"
asset_file = base_bath + r"\config\asset.txt"

stock_starter_file = base_bath + r"\starter\stock.start"
crypto_starter_file = base_bath + r"\starter\crypto.start"
trans_starter_file = base_bath + r"\starter\trans.start"

crypto_stream_file = base_bath + r"\stream\cryptostream.csv"
stock_stream_file = base_bath + r"\stream\stockstream.csv"


staged_path = base_bath + r"\staged"
staged_path_archive = base_bath + r"\staged\Archive"

tarns_path = base_bath + r"\trans"
tarns_path_archived = base_bath + r"\trans\Archive"


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
