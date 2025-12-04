from fastapi import FastAPI, UploadFile, File, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from hashing.hashing import generate_sha256_hash
from blockchain.store import store_hash_on_chain
from blockchain.verify import find_hash_on_chain

app = FastAPI()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
# ----------------------------------------------

# Models
class HashPayload(BaseModel):
    hash: str

# ------------------ OPTIONS FIX ------------------
@app.options("/register-hash")
async def register_hash_options():
    return Response(status_code=200)

@app.options("/verify-hash")
async def verify_hash_options():
    return Response(status_code=200)
# --------------------------------------------------


@app.post("/register-hash")
def register_hash(payload: HashPayload = Body(...)):
    txid = store_hash_on_chain(payload.hash)
    return {"stored_hash": payload.hash, "txid": txid}


@app.post("/verify-hash")
def verify_hash(payload: HashPayload = Body(...)):
    result = find_hash_on_chain(payload.hash)
    if result:
        return {"status": "authentic", "details": result}
    return {"status": "not_found"}


@app.post("/register-file")
async def register_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_hash = generate_sha256_hash(file_bytes)
    txid = store_hash_on_chain(file_hash)
    return {"filename": file.filename, "hash": file_hash, "txid": txid}


@app.post("/verify-file")
async def verify_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_hash = generate_sha256_hash(file_bytes)
    result = find_hash_on_chain(file_hash)
    if result:
        return {"status": "authentic", "hash": file_hash, "details": result}
    return {"status": "not_found", "hash": file_hash}
