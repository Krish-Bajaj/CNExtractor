import pickle

with open ('tickers.txt', 'rb') as file:
    stocks = pickle.load(file)

for stock in stocks:
    print(stock["ticker"])

