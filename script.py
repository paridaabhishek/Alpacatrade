import sys
import alpaca_trade_api as tradeapi
import os

# import matplotlib
print(sys.version)
print(sys.executable)


def greet(who_to_greet):
    greeting = "Hello ,{}".format(who_to_greet)
    return greeting


print(greet("world"))
print(greet("Corey"))
# tradeapi.REST.add_to_watchlist


name = input("Yeor name ?")
print("Hello, ! " + name)