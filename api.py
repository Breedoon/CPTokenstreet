from flask import Flask, jsonify, request, session
import pandas as pd
import os
import sqlite3
from uniswap import Uniswap

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = os.urandom(24)

UNISWAP_V = 2  # specify which version of Uniswap to use
PROVIDER = "https://ropsten.infura.io/v3/cfada245c0fa4dc9b5689accabd0cfc6"


@app.route('/api/v1/balance', methods=['GET'])
def balance():
    wallet = request.args.get("wallet")
    pk1 = request.args.get("pk")
    token = request.args.get("token")

    if wallet is not None:  # save to session if provided
        session['wallet'] = wallet
    else:
        wallet = session.get('wallet')

    if token is None:  # if token is not provided, returnETH
        token = 'ETH'

    try:
        conn = sqlite3.connect('api.db')
        wallet, pk2, token_addr = pd.read_sql(f"""SELECT wallets.address AS wallet, private_key, tokens.address AS token
                                                     FROM wallets CROSS JOIN tokens
                                                   WHERE wallets.address = '0x60Edfe106902d06A495CE807856647B3f0EdF6Fd'
                                                     AND tokens.symbol = 'TST';""", con=conn).values[0]
        private_key = pk1 + pk2

        uniswap = Uniswap(wallet, private_key, version=UNISWAP_V, provider=PROVIDER)

        bal = uniswap.get_token_balance(token_addr) / 1e18
    except Exception as e:
        return jsonify({'Error': str(e)}), 400

    return jsonify({'token': token, 'balance': bal})



if __name__ == '__main__':
    app.run(debug=True)