"""
    webqueries
"""
import csv
import os

COL_HEADERS = "date pair value".split(" ")
PAIRS = "btcusd usdeur btceur ethusd etheur eureur usdusd btcbtc etheth".split(" ")
SAVE_ALL_ANSWERS_FILE = "SAVE_ALL_ANSWERS.csv"

if "btceurhist/btceurhist" not in os.getcwd():  # corrects path during dev
    SAVE_ALL_ANSWERS_FILE = os.path.join("btceurhist", SAVE_ALL_ANSWERS_FILE)


def append(row, filename=SAVE_ALL_ANSWERS_FILE):
    """
    appends answer to cache file
    """
    tab_separated = ("\t".join(row)) + "\n"
    with open(filename, "a") as f:
        f.write(tab_separated)


def create_csv_file(col_headers=COL_HEADERS, filename=SAVE_ALL_ANSWERS_FILE):
    """
    write column headers
    """
    if os.path.isfile(filename):
        print("File '%s' exists already, doing nothing." % filename)
    else:
        append(col_headers)
        print("Done. File '%s' should exist now, check folder." % filename)


def read_cache_file(filename=SAVE_ALL_ANSWERS_FILE):
    """
    read in previous answers
    """
    cache = dict([(pairname, {}) for pairname in PAIRS])
    try:
        with open(filename, "r") as f:
            cache_raw = csv.reader(f, delimiter="\t")
            next(cache_raw)  # skip header row
            for row in cache_raw:
                cache[row[1]][row[0]] = row[2]  # duplicates overwritten anyway
    except FileNotFoundError:
        create_csv_file()
    return cache


def lookup(pair, date, cache):
    """
    query cache: if answer not existing, return None.
    """
    price = None
    prices = cache.get(pair, None)
    if prices:
        price = prices.get(date, None)
    return price


def insert(pair, date, price, cache):
    """
    insert answer into (transient, RAM) cache
    """
    cache[pair][date] = price


if __name__ == "__main__":
    create_csv_file()
