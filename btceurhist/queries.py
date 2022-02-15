"""
    webqueries
"""

import os
import pprint
import requests  # pip install requests

try:
    import rowcache
except Exception:
    import btceurhist.rowcache as rowcache

# open:
COINDESK_BTCUSD = "https://api.coindesk.com/v1/bpi/historical/close.json"\
                  "?start={startdate}&end={enddate}"

# open, but covers no weekends?
FOORILLA_USDEUR = "https://fxdata.foorilla.com/api/usdrates/"\
                  "?currency=EUR&date_min={startdate}&date_max={enddate}"

# 1000 per month are free:
OPENEXCHANGERATES_PATH = "OPENEXCHANGERATES"
if "btceurhist/btceurhist" not in os.getcwd():  # corrects path during dev
    OPENEXCHANGERATES_PATH = os.path.join("btceurhist", OPENEXCHANGERATES_PATH)
APP_ID = open(OPENEXCHANGERATES_PATH).read()
OXR_USDEUR = "https://openexchangerates.org/api/historical/{date}.json"\
             "?app_id={app_id}&symbols={symbols}"
OXR_USAGE = "https://openexchangerates.org/api/usage.json?app_id={app_id}"


def caller(url):
    try:
        r = requests.get(url)
        answer = r.json()
    except Exception as e:
        answer = "(%s) %s" % (type(e), e)

    return answer


def jsoner(j, jpath):
    if isinstance(j, str):
        return j  # then the requests.get had resulted in an error

    answer = j
    try:
        for dive in jpath:
            answer = answer[dive]
    except Exception as e:
        answer = "(%s) %s for %s" % (type(e), e, j)

    return answer


def btcusd(date, urltemplate=COINDESK_BTCUSD):
    # params={"startdate" :"2020-01-01","enddate" :"2020-01-05"}
    params = {"startdate": date, "enddate": date}
    url = urltemplate.format(**params)
    j = caller(url)
    price = jsoner(j, ['bpi', date])
    return price


def usdeur_foorilla(date, urltemplate=FOORILLA_USDEUR):
    # params={"startdate" :"2020-01-01","enddate" :"2020-01-05"}
    params = {"startdate": date, "enddate": date}
    url = urltemplate.format(**params)
    j = caller(url)
    # print (j)
    pricedict = jsoner(j, ['results'])
    if isinstance(pricedict, str):
        return pricedict  # error message
    price = jsoner(pricedict[0], ['value'])
    return price


def usdeur_oxr(date, urltemplate=OXR_USDEUR, app_id=APP_ID):
    # params={"startdate" :"2020-01-01","enddate" :"2020-01-05"}
    params = {"date": date, "app_id": app_id, "symbols": "EUR"}
    url = urltemplate.format(**params)
    # print (url)
    j = caller(url)
    # print (j)
    price = jsoner(j, ['rates', "EUR"])
    return price


usdeur = usdeur_oxr


def btceur(date):
    in_usd = btcusd(date)
    to_eur = usdeur(date)
    try:
        answer = float(in_usd) * float(to_eur)
    except Exception:
        answer = "cannot multiply: (%s, %s)" % (in_usd, to_eur)
    return answer
    return 10000


def oxr_usage(urltemplate=OXR_USAGE, app_id=APP_ID):
    params = {"app_id": app_id}
    url = urltemplate.format(**params)
    # print (url)
    j = caller(url)
    u = jsoner(j, ["data", "usage"])
    answer = pprint.pformat(u)
    # print (answer)
    return answer


CALLER = {"btcusd": btcusd,
          "usdeur": usdeur,
          "btceur": btceur
          }


def pairprice(pair, date):
    # print (pair, date)
    answer = "%s" % (CALLER[pair](date))
    rowcache.append([date, pair, answer])
    return answer


def test_all_queries():
    print(oxr_usage())
    """
    date="2021-03-15"; print (btcusd(date))
    date="2021-03-77"; print (btcusd(date))
    print (btcusd(date, urltemplate="ERROR_"+COINDESK_BTCUSD))
    print ()
    date="2021-01-01"; print (usdeur(date))
    date="2021-03-77"; print (usdeur(date))
    print ()
    date="2021-03-15"; print (btceur(date))
    date="2021-03-77"; print (btceur(date))
    print()
    """
    print(pairprice("btcusd", "2020-01-01"))
    print(pairprice("usdeur", "2020-01-01"))
    print(pairprice("btceur", "2020-01-01"))


if __name__ == '__main__':
    test_all_queries()
