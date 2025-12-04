from .config import w3, SENDER

def find_hash_on_chain(target_hash: str):
    latest = w3.eth.block_number

    for block_num in range(latest, -1, -1):  
        block = w3.eth.get_block(block_num, full_transactions=True)

        for tx in block.transactions:

            
            if tx["from"].lower() != SENDER.lower():
                continue

            
            if not tx["input"] or tx["input"] == "0x":
                continue

            
            try:
                hexdata = tx["input"][2:]     # remove "0x"
                decoded = bytes.fromhex(hexdata).decode("utf-8")
            except:
                continue

            
            if decoded == target_hash:
                return {
                    "owner": tx["from"],
                    "tx": tx["hash"].hex(),
                    "block": block_num,
                    "stored_hash": decoded
                }

    return None
