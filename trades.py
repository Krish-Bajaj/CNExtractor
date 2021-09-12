import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pickle

stocks = []
stock_name = "(.*)\("
stock_ticker = "\((.*)\)"

urls = ['https://in.finance.yahoo.com/quote/TECHM.NS', 'https://in.finance.yahoo.com/quote/ZENSARTECH.NS?p=ZENSARTECH.NS&.tsrc=fin-srch']

for url in urls:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # the Headers part allows us to by pass mod_security which blocks crawlers
    webpage = urlopen(req)

    soup = BeautifulSoup(webpage, "html.parser")
    stock = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text

    stocks.append({ "name": re.findall(stock_name, stock)[0].strip(), "ticker": re.findall(stock_ticker, stock)[0] })

with open('tickers.txt', 'wb') as file:
    pickle.dump(stocks, file)
print(stocks)
