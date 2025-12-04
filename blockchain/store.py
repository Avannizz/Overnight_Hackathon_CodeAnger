from .config import w3, PRIVATE_KEY, SENDER

def store_hash_on_chain(file_hash: str):
    data_hex = "0x" + file_hash.encode().hex()

    tx = {
        "nonce": w3.eth.get_transaction_count(SENDER),
        "to": SENDER,
        "value": 0,
        "gas": 150000,
        "gasPrice": w3.to_wei("1", "gwei"),
        "data": data_hex,
        "chainId": w3.eth.chain_id,
    }

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()
