### Overview

This implementation defines the new token and the logic for buying/minting tokens in the same contract. The token is minted in exchange for a base token, likely an Euro Stablecoin, at the mint price rate. The base token and minting price can be changed at any time.

For using the funds or issuing a refund, the base tokens would be transferred out of the contract using send_base_token. This is the most important function to test before production, as it could lock the funds in the contract or make them vulnerable to malicious actors.

### Basic functionalities

Creating the token*:
1. Deploy token contract
2. Set the base token with set_base_token
3. Set the minting price with set_mint_price
4. Whitelist addresses

Whitelisting an address*:
1. Call whitelist function from the owner address

Revoke whitelisting*:
1. Set an address to received the tokens held by the revoked address
2. Call revoke_whitelist with the target address

Creating the Liquidity Pool*:
1. Create the LP using the normal platform UI or API
2. Whitelist the LP contract

Buying tokens:
1. Get whitelisted
2. Allow the contract to access base_token either manually or with allow_base_token
3. Buy the token with buy_token. It will automatically debit the base_token and credit the newly minted token.

*-Needs to be done from the owner address