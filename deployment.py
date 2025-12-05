from solcx import compile_source, install_solc
from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
account = w3.eth.accounts[0]

install_solc("0.8.0")

with open("MediaRegistry.sol", "r") as f:
    source = f.read()

compiled = compile_source(source, solc_version="0.8.0")
contract_id, interface = compiled.popitem()

MediaRegistry = w3.eth.contract(
    abi=interface["abi"],
    bytecode=interface["bin"]
)

tx_hash = MediaRegistry.constructor().transact({"from": account})
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract deployed at:", receipt.contractAddress)

with open("MediaRegistry_abi.json", "w") as f:
    json.dump(interface["abi"], f)
