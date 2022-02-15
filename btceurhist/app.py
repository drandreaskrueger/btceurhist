"""
bottle app

endpoints:

    /<pair>/<date> for pairs: see queries.py

    /
    /home
    /usage
    /examples
"""

import os
import bottle  # pip install bottle
from bottle import route, template, redirect, run

try:
    from . import queries
except ImportError:
    import queries  # type: ignore[no-redef]

VERSION_PATH = "VERSION"

if "btceurhist/btceurhist" in os.getcwd():  # corrects path for local machine
    bottle.TEMPLATE_PATH.insert(0, '../views')
    # STATIC_ROOT = os.path.join("..", STATIC_ROOT)
else:
    VERSION_PATH = os.path.join("btceurhist", VERSION_PATH)
    # STATIC_ROOT = 'static'

VERSION = open(VERSION_PATH).read()

#                                     static endpoints


@route('/home')
def show_home():
    return template('home', version=VERSION)


@route('/')
def handle_root_url():
    redirect('/home')


@route('/output')
def show_output():
    output = "to be generated"
    return template('output', output=output)


@route('/usage')
def show_oxr_usage():
    usage = queries.oxr_usage()
    return template('usage', usage=usage)


@route('/examples')
def show_examples():
    return template('examples')

#                               endpoints with query answers


@route('/price/<pair>/<date>')
def give_price(pair, date):
    return queries.pairprice(pair, date)

#                               runloop


def server():
    if "heroku" in os.environ.get('PYTHONHOME', ''):
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        run(host='localhost', port=8080, debug=True)


if __name__ == '__main__':
    server()
