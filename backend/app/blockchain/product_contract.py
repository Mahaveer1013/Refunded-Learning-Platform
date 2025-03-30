from .web3_config import w3


# Contract details
contract_address = "0x670414990B56fd78EE2A654795C4E15651470306"  # Replace with your deployed contract address
produceAbi = [
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

produceContract = w3.eth.contract(address=contract_address, abi=produceAbi)
