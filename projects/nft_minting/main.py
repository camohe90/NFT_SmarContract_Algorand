import os

import json
import hashlib

from dotenv import load_dotenv

from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
    AssetFreezeParams,


)

import algokit_utils


#import seedphrase from the .env
PASSPHRASE = os.environ.get("PASSPHRASE")

print("--------------------------------------------")
print("Processing account...")

#Connect to testnet

algorand = AlgorandClient.test_net()
# Retrieve the account from seedphrase
account = algokit_utils.get_account_from_mnemonic(PASSPHRASE)

print(account.private_key)

# JSON file
dir_path = os.path.dirname(os.path.realpath(__file__))
f = open (dir_path + '/metadata.json', "r")

# Reading from file
metadataJSON = json.loads(f.read())
metadataStr = json.dumps(metadataJSON)
print(metadataStr)

#Creating the metadata_hash
hash = hashlib.new("sha512_256")
hash.update(b"arc0003/amj")
hash.update(metadataStr.encode("utf-8"))
json_metadata_hash = hash.digest()

print(type(json_metadata_hash))

# sent_txn = algorand.send.asset_create(
#     AssetCreateParams(
#         sender=account.address,
#         signer=account.signer,
#         total= 1,
#         asset_name="Hally",
#         unit_name="HALL",
#         manager=account.address,
#         clawback=account.address,
#         freeze=account.address,
#         url="https://gateway.pinata.cloud/ipfs/QmTURg66KbuZqFgajPhLnRaaMnpCVZcmhR1xgc3xaGGzUL", # URL to the metada file on IPFS 
#         metadata_hash=json_metadata_hash,
#         decimals=0
        
#     )
# )

# asset_id= sent_txn["confirmation"]["asset-index"]
# print(asset_id)
