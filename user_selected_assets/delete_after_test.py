import ast
import json
from datetime import datetime
from os import path
import os


#######################import required functions#######################

from paths import *


def get_stocks(stock_file):
    # print([line.strip() for line in open(stock_file, "r")])
    return [line.strip() for line in open(stock_file, "r")]


print(get_stocks(r"C:\Users\abhis\DATA\Alpeca\config\stocksBkp.txt"))


print(os.stat(stock_file).st_size)
