from flask import Flask, jsonify, request, session
import pandas as pd
import os
import sqlite3
from uniswap import Uniswap

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = os.urandom(32)

UNISWAP_V = 2  # specify which version of Uniswap to use
PROVIDER = "https://ropsten.infura.io/v3/cfada245c0fa4dc9b5689accabd0cfc6"


@app.route('/api/v1/balance', methods=['GET'])
def balance():
    wallet, pk1, token, _ = process_args(request.args.get("wallet"), request.headers.get('authorization'),
                                         request.args.get("token"))

    try:
        wallet, private_key, token1_addr, _ = get_credentials(wallet, pk1, token)
        uniswap = Uniswap(wallet, private_key, version=UNISWAP_V, provider=PROVIDER)
        bal = uniswap.get_token_balance(token1_addr) / 1e18
    except Exception as e:
        return jsonify({'Error': str(e)}), 400

    return jsonify({'token': token, 'balance': bal})


@app.route('/api/v1/price', methods=['GET'])
def price():
    return exchange(make_transaction=False)  # ie, just check the price


@app.route('/api/v1/trade', methods=['GET', 'POST'])
def trade():
    return exchange(make_transaction=request.method == 'POST')  # transaction only if POST


def exchange(make_transaction=False):
    if request.args.get("sell-amt") is not None:  # if given sell amt, assume it's price input
        sell_amt = True
        amt = request.args.get("sell-amt")
    else:  # not given sell amt, assume given buy-amt
        sell_amt = False
        amt = request.args.get("buy-amt")
    wallet, pk1, sell_token, buy_token, amt = process_args(request.args.get("wallet"),
                                                           request.headers.get('authorization'),
                                                           request.args.get("sell-token"),
                                                           request.args.get("buy-token"),
                                                           amt=amt)
    sell_price, buy_price = amt / 1e18, amt / 1e18  # init with given amount

    try:
        wallet, private_key, sell_token_addr, buy_token_addr = get_credentials(wallet, pk1, sell_token, buy_token)
        uniswap = Uniswap(wallet, private_key, version=UNISWAP_V, provider=PROVIDER)
        if not make_transaction:  # just checking the price
            if sell_amt:  # specified sell (input) price
                buy_price = uniswap.get_price_input(sell_token_addr, buy_token_addr, amt) / 1e18
            else:
                sell_price = uniswap.get_price_output(sell_token_addr, buy_token_addr, amt) / 1e18
        else:  # making a transaction (buying or selling)
            if sell_amt:  # specified sell (input) price
                transaction_id = uniswap.make_trade(sell_token_addr, buy_token_addr, amt)
            else:
                transaction_id = uniswap.make_trade_output(sell_token_addr, buy_token_addr, amt)

    except Exception as e:
        return jsonify({'Error': str(e)}), 400

    if not make_transaction:  # just checking the price
        return jsonify({
            'sell-token': sell_token,
            'buy-token': buy_token,
            'sell-amt': sell_price,
            'buy-amt': buy_price
        })
    else:  # made a transaction
        return jsonify({
            'transaction-id': transaction_id.hex()
        })


def process_args(wallet, pk1, token1, token2=None, amt=None):
    if wallet is not None:  # save to session if provided
        session['wallet'] = wallet
    else:
        wallet = session.get('wallet')

    if token1 is None:  # if token is not provided, return ETH
        token1 = 'ETH'

    if token2 is None:
        token2 = 'ETH'

    return_args = wallet, pk1, token1, token2

    if amt is not None:
        amt = int(float(amt) * 1e18)
        return_args = return_args + (amt,)

    return return_args


def get_credentials(wallet_addr, pk1, token1='TST', token2='ETH'):
    sql = f"""
        SELECT w.address AS wallet, private_key, t1.address AS token1_addr, t2.address AS token2_addr
        FROM wallets w
                 CROSS JOIN tokens t1
                 CROSS JOIN tokens t2
        WHERE w.address = '{wallet_addr}'
          AND t1.symbol = '{token1}'
          AND t2.symbol = '{token2}';
    """
    conn = sqlite3.connect('api.db')
    wallet, pk2, token1_addr, token2_addr = pd.read_sql(sql, con=conn).values[0]
    private_key = pk1 + pk2
    return wallet, private_key, token1_addr, token2_addr


if __name__ == '__main__':
    app.run(debug=True)
