from web3 import Web3

acct = Web3().eth.account.create()

print("=== NEW TESTNET WALLET ===")
print("PRIVATE KEY:", acct.key.hex())
print("ADDRESS    :", acct.address)
print("===========================")
print("Fund this address with Sepolia ETH:")
print("https://sepoliafaucet.com")
