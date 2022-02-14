"""
    webqueries
"""

import os

COLUMN_HEADERS="date pair value".split(" ")

SAVE_ALL_ANSWERS_FILE="SAVE_ALL_ANSWERS.csv"
if "btceurhist/btceurhist" not in os.getcwd(): # corrects path for local machine
    SAVE_ALL_ANSWERS_FILE=os.path.join("btceurhist", SAVE_ALL_ANSWERS_FILE)

def append(row, filename=SAVE_ALL_ANSWERS_FILE):
    tab_separated = ("\t".join(row))+"\n"
    with open(SAVE_ALL_ANSWERS_FILE, "a") as f:
        f.write(tab_separated)
    
def create_csv_file(column_headers=COLUMN_HEADERS, filename=SAVE_ALL_ANSWERS_FILE):
    if os.path.isfile(filename):
        print ("File '%s' exists already, doing nothing." % filename)
    else:
        append(column_headers)
        print("Done. File '%s' should exist now, please check folder." % filename)

if __name__ == '__main__':
    create_csv_file()
