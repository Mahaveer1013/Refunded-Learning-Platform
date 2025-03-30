from fastapi import APIRouter, HTTPException
from blockchain.product_contract import produceContract
from blockchain.web3_config import w3
from schemas.produce_schemas import AddProduceRequest


produce_routes = APIRouter(
    prefix="/produce",
    tags=["produce"],
)

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
@produce_routes.post("/add-produce/")
async def add_produce_endpoint(request: AddProduceRequest):
    try:
        print("Adding produce...")
        account = w3.to_checksum_address(request.account)
        print(f"Using account: {account}")
        nonce = w3.eth.get_transaction_count(account)
        print(f"Nonce: {nonce}")

        transaction = produceContract.functions.addProduce(
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
@produce_routes.get("/get-all-produce/")
async def get_all_produce_endpoint():
    try:
        print("Calling getAllProduces() on the produceContract...")
        result = produceContract.functions.getAllProduces().call()
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
