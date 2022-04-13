import os
import json
from solcx import compile_standard, install_solc 
from web3 import Web3 
from dotenv import load_dotenv

load_dotenv()

install_solc('0.6.0')

with open('storage.sol', 'r') as file:
    storage_file = file.read()
    # print(storage_file) 

compiled_storage = compile_standard({
    'language': "Solidity",
    "sources": {"storage.sol":{"content": storage_file}},
    "settings": {"outputSelection":{"*": {"*":['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']}}},
},
solc_version='0.6.0'
)

with open('compiled_code.json','w') as file:
    json.dump(compiled_storage, file)

# get the bytecode
bytecode = compiled_storage['contracts']['storage.sol']['Storage']['evm']['bytecode']['object']

# get the application binary interface
abi = compiled_storage['contracts']['storage.sol']['Storage']['abi'] 

w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/c7d0af5c9bd444afac8aa592b1920312'))
chain_id = 4
my_address = '0xc99972006559e16Ced96D5caF7783378071AC68C'
private_key = os.getenv('PRIVATE_KEY')

# Create another instance of the contract using its abi and bytecode in python
Storage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(Storage)

# Get the recent transaction nonce 
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# A transaction deploys a contract to the blockchain...
# 1. Build a transaction
# 2. Sign the transaction 
# 3. Send the transaction

print("Deploying A Contract ...")
transaction = Storage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price,'chainId': chain_id, "from": my_address, "nonce": nonce})
# print(transaction)

signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_transaction)

transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print("Contract Deployed...")

# Working with the contract...
# we need the ...
# 1. Contract Address
# 2. Contract ABI

# create a new Storage object...
storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
# when making transaction in a blockchain , there are twoways to interact ...
# 1. call --> Simulate making a call and getting a return value
# example...
print(storage.functions.retrieve().call())

# 2. transact --> Make a state change

# lets build a new transaction to actually store some value into the contract... since we want to make a transaction we have to go through the same process as when we deployed the contract ...
print("Updating A Contract ...")
# Making a State Change...
store_transaction = storage.functions.store(7).buildTransaction({"gasPrice": w3.eth.gas_price,'chainId': chain_id, "from": my_address, "nonce": nonce + 1})

signed_store_transc = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
sent_store_transc = w3.eth.send_raw_transaction(signed_store_transc.rawTransaction)
store_transc_receipt =w3.eth.wait_for_transaction_receipt(sent_store_transc)
print("Contract Updated...")
print(storage.functions.retrieve().call())