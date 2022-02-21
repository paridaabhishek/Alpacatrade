import ast
import json
from datetime import datetime
from os import path
import os
import pandas as pd


#######################import required functions#######################

from paths import *


# def get_stocks(stock_file):
#     # print([line.strip() for line in open(stock_file, "r")])
#     return [line.strip() for line in open(stock_file, "r")]


# print(get_stocks(r"C:\Users\abhis\DATA\Alpeca\config\stocksBkp.txt"))


# print(os.stat(stock_file).st_size)

df = pd.read_csv(
    r"C:\Users\abhis\DATA\Alpeca\stream\Archive\cryptostream_20220221_10_17.csv",
    index_col=None,
)
print(df)

df = df.iloc[-1:]

print(df)

df.to_csv(
    r"C:\Users\abhis\DATA\Alpeca\stream\Archive\cryptostream_20220221_10_17.csv",
    index=False,
    header=True,
)
