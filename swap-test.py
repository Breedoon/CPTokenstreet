from uniswap import Uniswap

address = "0x03C91a10901EB0E511B572c50c01DBEBA0d526Db"  # or None if you're not going to make transactions
private_key = "74565d008eabcff07caec1b4b7072e888e8d02aab5ba4149b3977e80d3f37408"  # or None if you're not going to make transactions
version = 3  # specify which version of Uniswap to use
provider = "HTTP://172.31.240.1:7545"  # can also be set through the environment variable `PROVIDER`
uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)

# %%
uniswap.make_trade()
uniswap.get_eth_balance()
