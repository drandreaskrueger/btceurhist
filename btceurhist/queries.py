"""
    webqueries
"""

import requests # pip install requests

def btcusd(date):
    return 12345

def usdeur(date):
    return 1.15

def btceur(date):
    return 10000

CALLER = {"btcusd": btcusd,
          "usdeur": usdeur,
          "btceur": btceur
          }

def pairprice(pair, date):
    print (pair, date)
    return "%s" % CALLER[pair](date)
    

def test_all_queries():
    date="2021-03-15"
    print (btcusd(date))
    print (usdeur(date))
    print (btceur(date))
    print (pairprice("btceur", "2020-01-01"))
    

if __name__ == '__main__':
    test_all_queries()
    