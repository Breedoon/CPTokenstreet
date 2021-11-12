from uniswap import Uniswap

# rapsen
address = "0x60Edfe106902d06A495CE807856647B3f0EdF6Fd"  # or None if you're not going to make transactions
private_key = "1470311f9a955c0d9eae56d60d740bd66161c79f8dbadfc5b08d9666dbea433b"  # or None if you're not going to make transactions
version = 2  # specify which version of Uniswap to use
provider = "https://ropsten.infura.io/v3/cfada245c0fa4dc9b5689accabd0cfc6"

# local ganache
# address = "0x03C91a10901EB0E511B572c50c01DBEBA0d526Db"  # or None if you're not going to make transactions
# private_key = "74565d008eabcff07caec1b4b7072e888e8d02aab5ba4149b3977e80d3f37408"  # or None if you're not going to make transactions
# version = 2  # specify which version of Uniswap to use
# provider = "HTTP://172.31.240.1:7545"  # can also be set through the environment variable `PROVIDER`

uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)

# %%
eth = "0x0000000000000000000000000000000000000000"
# tst = "0xbF8Da1e5a773Aa2466F1Da64F143aD12857076bb"  # local ganache
tst = "0x9D0Cfd3EC8e18b3C3055fC7F914c82FDc28efc54"

# %%
uniswap.get_eth_balance() / 1e18
uniswap.get_token_balance(tst) / 1e18

# %%
uniswap.get_token(tst)

# %%
pool = '0x6426D297A5CfeC9A56eB6E3921e260c753af09d6'
uniswap.get_price_input(eth, tst, 10 * 10 ** 18) / 1e18

# %%
r = uniswap.make_trade_output(eth, tst, 10 * 10 ** 18)
r.hex()
# %%

address = "0x9978FC973Fe8CBC87dF923626e0CeA306C17aeb3"
private_key = "8fb92dd2b1affe18655c7edafe2c9285c63115b9172f37f38ee030b4cd5469f4"
us2 = Uniswap(address=address, private_key=private_key, version=version, provider=provider)

# %%
us2.get_eth_balance() / 1e18
us2.get_token_balance(tst) / 1e18

us2.make_trade(tst, eth, us2.get_token_balance(tst))
us2.make_trade(eth, tst, us2.get_eth_balance() // 2)
