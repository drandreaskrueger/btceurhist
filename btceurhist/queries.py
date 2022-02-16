"""
    webqueries
"""

import os
import pprint

import requests  # pip install requests

try:
    from . import rowcache
except ImportError:  # we also want to run `python3 queries.py` separately, so:
    import rowcache  # type: ignore[no-redef]

# open:
COINDESK_BTCUSD = (
    "https://api.coindesk.com/v1/bpi/historical/close.json"
    "?start={startdate}&end={enddate}"
)

# open, but covers no weekends?
FOORILLA_USDEUR = (
    "https://fxdata.foorilla.com/api/usdrates/"
    "?currency=EUR&date_min={startdate}&date_max={enddate}"
)

# OpenExchangeRates.com
OXR_USDEUR = (
    "https://openexchangerates.org/api/historical/{date}.json"
    "?app_id={app_id}&symbols={symbols}"
)
OXR_ALTCOINS = (
    "https://openexchangerates.org/api/historical/2020-07-10.json"
    "?app_id={app_id}&symbols={symbols}&show_alternative=1"
)
OXR_USAGE = "https://openexchangerates.org/api/usage.json?app_id={app_id}"
# 1000 per month are free, store your APP_ID in this file:
OPENEXCHANGERATES_PATH = "OPENEXCHANGERATES"
if "btceurhist/btceurhist" not in os.getcwd():  # corrects path during dev
    OPENEXCHANGERATES_PATH = os.path.join("btceurhist", OPENEXCHANGERATES_PATH)
try:
    APP_ID = open(OPENEXCHANGERATES_PATH).read()
except FileNotFoundError:
    print(
        "ERROR: You must store your openexchangerates.com "
        "APP_ID into file: '%s'" % OPENEXCHANGERATES_PATH
    )
    APP_ID = "App_ID-is-missing"


CACHE = rowcache.read_cache_file()  # yes, as a global variable, I am bad lol


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
    price = jsoner(j, ["bpi", date])
    return price


def usdeur_foorilla(date, urltemplate=FOORILLA_USDEUR):
    # params={"startdate" :"2020-01-01","enddate" :"2020-01-05"}
    params = {"startdate": date, "enddate": date}
    url = urltemplate.format(**params)
    j = caller(url)
    # print (j)
    pricedict = jsoner(j, ["results"])
    if isinstance(pricedict, str):
        return pricedict  # error message
    price = jsoner(pricedict[0], ["value"])
    return price


def usdeur_oxr(date, urltemplate=OXR_USDEUR, app_id=APP_ID):
    # params={"startdate" :"2020-01-01","enddate" :"2020-01-05"}
    params = {"date": date, "app_id": app_id, "symbols": "EUR"}
    url = urltemplate.format(**params)
    # print (url)
    j = caller(url)
    # print (j)
    price = jsoner(j, ["rates", "EUR"])
    return price


usdeur = usdeur_oxr


def coineur(date, coinusd_fn=btcusd):
    in_usd = coinusd_fn(date)
    to_eur = usdeur(date)
    try:
        answer = float(in_usd) * float(to_eur)
    except Exception:
        answer = "cannot multiply: (%s, %s)" % (in_usd, to_eur)
    return answer


def btceur(date):
    return coineur(date, coinusd_fn=btcusd)


def oxr_usage(urltemplate=OXR_USAGE, app_id=APP_ID):
    params = {"app_id": app_id}
    url = urltemplate.format(**params)
    j = caller(url)
    u = jsoner(j, ["data", "usage"])
    answer = pprint.pformat(u)
    return answer


def altcoinusd(altcoin, date, urltemplate=OXR_ALTCOINS, app_id=APP_ID):
    params = {"date": date, "app_id": app_id, "symbols": altcoin}
    url = urltemplate.format(**params)
    j = caller(url)
    price_inverse = jsoner(j, ["rates", altcoin.upper()])
    if isinstance(price_inverse, str):
        return price_inverse
    return 1.0 / float(price_inverse)


def ethusd(date, urltemplate=OXR_ALTCOINS, app_id=APP_ID):
    return altcoinusd("ETH", date, urltemplate, app_id)


def etheur(date):
    return coineur(date, coinusd_fn=ethusd)


CALLER = {"usdeur": usdeur,
          "btcusd": btcusd, "btceur": btceur,
          "ethusd": ethusd, "etheur": etheur}


def pairprice(pair, date, cache=CACHE):
    """
    Tries to find the price for that date in the cache.

    If not there yet, query the internet.
    If answer is numerical (not string=error), then
      append answer to cache log, and
      insert into RAM cache.

    Returns price (or error message) for (pair, date).
    """
    # print (pair, date)
    if pair not in CALLER:
        return "ERROR: pair '%s' not implemented yet." % pair

    cached_answer = rowcache.lookup(pair, date, cache)
    if cached_answer:
        # print("recycled old answer!")
        return cached_answer

    answer_string = CALLER[pair](date)
    try:
        price = str(float(answer_string))  # test whether number - or error
        rowcache.append([date, pair, price])
        rowcache.insert(pair, date, price, cache)
        # print("new answer appended to file cache & inserted into RAM cache")
    except Exception:
        price = answer_string  # error message

    return price


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
    date = "2021-01-01"; print(ethusd(date))
    date = "2021-01-01"; print(etheur(date))
    date = "2021-01-01"; print(usdeur(date))
    print()
    exit()
    """
    print(pairprice("btcusd", "2020-01-01"))
    print(pairprice("usdeur", "2020-01-01"))
    print(pairprice("btceur", "2020-01-01"))
    print(pairprice("ethusd", "2020-01-01"))
    print(pairprice("etheur", "2020-01-01"))


if __name__ == "__main__":
    test_all_queries()
