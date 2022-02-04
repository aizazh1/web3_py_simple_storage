from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "evm.bytecode", "metadata", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiledCode.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to rinkeby using infura
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/d8e837490e2e4e5e8c1c7b9a0160a376")
)
chainId = 4
my_address = os.getenv("WALLET_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")  # append 0x to start of private key

# create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chainId,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# 2. Sign the transaction
signedTransaction = w3.eth.account.signTransaction(transaction, private_key)

# 3. Send the transaction
transaction_hash = w3.eth.sendRawTransaction(signedTransaction.rawTransaction)
print("Deploying contract...")
# 4. Wait for the transaction to be mined
transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
print("Contract deployed!")

# Working with the contract
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

# Call -> Simulate making a call to the contract, no state change
# Transact -> Make a state change to the contract

print("Updating contract...")
store_transaction = simple_storage.functions.store(42).buildTransaction(
    {
        "chainId": chainId,
        "from": my_address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_store_transaction = w3.eth.account.signTransaction(
    store_transaction, private_key
)
store_transaction_hash = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction
)
store_transaction_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)
print("Contract updated!")

print(simple_storage.functions.retrieve().call())
