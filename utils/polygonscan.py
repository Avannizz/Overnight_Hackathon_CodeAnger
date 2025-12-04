import requests
from blockchain.config import SENDER

ETHERSCAN_API_KEY = "4UP546QIG8VBNI21R4TFB27XGH8GM24EBP"

BASE_URL = "https://api-sepolia.etherscan.io/api"


def fetch_transactions():
    params = {
        "module": "account",
        "action": "txlist",
        "address": SENDER,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    resp = requests.get(BASE_URL, params=params)
    data = resp.json()

    
    if data.get("status") != "1":
        return []

    return data["result"]
