from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web3 import Web3
import uvicorn


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    raise Exception("Failed to connect to Ganache")

print("Connected to Ganache!")

# Contract details
contract_address = "0x670414990B56fd78EE2A654795C4E15651470306"  # Replace with your deployed contract address
abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "_farmerName", "type": "string"},
            {"internalType": "string", "name": "_cropName", "type": "string"},
            {"internalType": "uint256", "name": "_quantity", "type": "uint256"},
            {"internalType": "string", "name": "_location", "type": "string"},
        ],
        "name": "addProduce",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "getProduce",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "string", "name": "", "type": "string"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getAllProduces",
        "outputs": [
            {"internalType": "string[]", "name": "", "type": "string[]"},
            {"internalType": "string[]", "name": "", "type": "string[]"},
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
            {"internalType": "string[]", "name": "", "type": "string[]"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_address, abi=abi)

# Pydantic model for request validation
class AddProduceRequest(BaseModel):
    farmer_name: str
    crop_name: str
    quantity: int
    location: str
    account: str
    private_key: str

# Helper function to convert transaction receipt to JSON-serializable format
def serialize_transaction_receipt(txn_receipt):
    return {
        "transactionHash": txn_receipt["transactionHash"].hex(),
        "blockHash": txn_receipt["blockHash"].hex(),
        "blockNumber": txn_receipt["blockNumber"],
        "contractAddress": txn_receipt["contractAddress"],
        "cumulativeGasUsed": txn_receipt["cumulativeGasUsed"],
        "effectiveGasPrice": txn_receipt["effectiveGasPrice"],
        "from": txn_receipt["from"],
        "gasUsed": txn_receipt["gasUsed"],
        "logs": txn_receipt["logs"],
        "logsBloom": txn_receipt["logsBloom"].hex(),
        "status": txn_receipt["status"],
        "to": txn_receipt["to"],
        "transactionIndex": txn_receipt["transactionIndex"],
        "type": txn_receipt["type"],
    }



# Add produce details
@app.post("/add-produce/")
async def add_produce_endpoint(request: AddProduceRequest):
    try:
        print("Adding produce...")
        account = w3.to_checksum_address(request.account)
        print(f"Using account: {account}")
        nonce = w3.eth.get_transaction_count(account)
        print(f"Nonce: {nonce}")

        transaction = contract.functions.addProduce(
            request.farmer_name, request.crop_name, request.quantity, request.location
        ).build_transaction(
            {
                "chainId": 1337,
                "gas": 2000000,
                "gasPrice": w3.to_wei("50", "gwei"),
                "nonce": nonce,
            }
        )
        print("Transaction built successfully.")

        signed_txn = w3.eth.account.sign_transaction(transaction, request.private_key)
        print("Transaction signed successfully.")

        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction sent. Hash: {txn_hash.hex()}")

        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        print("Transaction confirmed.")
        return {"transaction_receipt": serialize_transaction_receipt(txn_receipt)}
    except Exception as e:
        print(f"Error: {e}")  # Debugging statement
        raise HTTPException(status_code=400, detail=str(e))

# Get all produce details
@app.get("/get-all-produce/")
async def get_all_produce_endpoint():
    try:
        print("Calling getAllProduces() on the contract...")
        result = contract.functions.getAllProduces().call()
        print("Result from getAllProduces():", result)

        farmer_names, crop_names, quantities, locations = result

        produces = []
        for i in range(len(farmer_names)):
            produces.append({
                "farmer_name": farmer_names[i],
                "crop_name": crop_names[i],
                "quantity": quantities[i],
                "location": locations[i],
            })

        print("Formatted produces data:", produces)
        return {"produces": produces}
    except Exception as e:
        print(f"Error in /get-all-produce/: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to IIIT Jabalpur Hackathon Backend!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}