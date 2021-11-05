from uniswap import Uniswap

address = "0x03C91a10901EB0E511B572c50c01DBEBA0d526Db"  # or None if you're not going to make transactions
private_key = "74565d008eabcff07caec1b4b7072e888e8d02aab5ba4149b3977e80d3f37408"  # or None if you're not going to make transactions
version = 1  # specify which version of Uniswap to use
provider = "HTTP://172.31.240.1:7545"  # can also be set through the environment variable `PROVIDER`
uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)

# %%
uniswap.get_eth_balance()


# %%
eth = "0x0000000000000000000000000000000000000000"
tst = "0xbF8Da1e5a773Aa2466F1Da64F143aD12857076bb"

# %%
uniswap.get_token_balance(tst)

# %%
uniswap.get_token(tst)


# %%
uniswap.get_price_input(eth, tst, 10)
