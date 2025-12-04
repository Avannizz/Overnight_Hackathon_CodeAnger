from web3 import Web3


RPC_URL = "http://127.0.0.1:8545"

PRIVATE_KEY = "0x6dcf2653abe737d313de2864decadba088c6a42b81804b8766ee54f02cd9045b"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise RuntimeError("Could not connect to local Ganache blockchain")

ACCOUNT = w3.eth.account.from_key(PRIVATE_KEY)
SENDER = ACCOUNT.address

print("Connected to local chain")
print("Wallet address:", SENDER)
print("Chain ID:", w3.eth.chain_id)  
