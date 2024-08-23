from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    PayParams
)


import os
import algokit_utils 

import json
import hashlib
from algokit_utils.beta.account_manager import AddressAndSigner

from smart_contracts.artifacts.nft_minting.nft_minting_client import NftMintingClient

from algosdk.atomic_transaction_composer import TransactionWithSigner


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

algorand = AlgorandClient.default_local_net()
account = algorand.account.random()

# import dispenser from KMD
dispenser = algorand.account.dispenser()
print(dispenser.address)

#Create a wallet for the creator of the token
creator = algorand.account.random()
print(creator.address)

#Get account info about creator
print(algorand.account.get_information(creator.address))

#Send Algos
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

app_client = NftMintingClient(
    algod_client = algorand.client.algod,
    sender = creator.address,
    signer= creator.signer,
    app_id = 1006
)

buyer_txn = algorand.transactions.payment(
        PayParams(
            sender= creator.address,
            receiver= NftMintingClient.app_address,
            amount= 200_000,
        )
    )

sp = algorand.client.algod.suggested_params()
sp.fee = 1000

response = app_client.mint_nft(
    unit_name="hall",
    asset_name="hally demo",
    metadata_hash=json_metadata_hash,
    url="https://gateway.pinata.cloud/ipfs/QmTURg66KbuZqFgajPhLnRaaMnpCVZcmhR1xgc3xaGGzUL",
    buyer_txn=TransactionWithSigner(txn=buyer_txn, signer= creator.signer),
    transaction_parameters=algokit_utils.TransactionParameters(
            sender=creator.address,
            signer=creator.signer,
            suggested_params=sp
        ),

)

print(f"Called rite on {app_client.app_id}")
print(f"wreceived: {response.return_value}")
