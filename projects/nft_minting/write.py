import hashlib
import json
import os

import algokit_utils
from algokit_utils.beta.algorand_client import AlgorandClient, PayParams
from algosdk.atomic_transaction_composer import TransactionWithSigner
from dotenv import load_dotenv

from smart_contracts.artifacts.nft_minting.nft_minting_client import NftMintingClient

# JSON file
dir_path = os.path.dirname(os.path.realpath(__file__))
f = open (dir_path + '/metadata.json', "r")

# Reading from file
metadata_JSON = json.loads(f.read())
metadata_str = json.dumps(metadata_JSON)
print(metadata_str)

#Creating the metadata_hash
hash_file = hashlib.new("sha512_256")
hash_file.update(b"arc0003/amj")
hash_file.update(metadata_str.encode("utf-8"))
json_metadata_hash = hash_file.digest()


load_dotenv()
PASSPHRASE = os.environ.get("PASSPHRASE")

print("Processing account...")

algorand = AlgorandClient.test_net()
creator = algokit_utils.get_account_from_mnemonic(PASSPHRASE)

app_client = NftMintingClient(
    algod_client = algorand.client.algod,
    sender = creator.address,
    signer= creator.signer,
    app_id =   717073267
)


buyer_txn = algorand.transactions.payment(
        PayParams(
            sender= creator.address,
            signer= creator.signer,
            receiver= app_client.app_address,
            amount= 200_000,
        )
    )

sp = algorand.client.algod.suggested_params()
sp.flat_fee = True
sp.fee = 2_000

response = app_client.mint_nft(
    unit_name="hall",
    asset_name="hally demo",
    metadata_hash=json_metadata_hash,
    url="https://gateway.pinata.cloud/ipfs/QmWKnX5aA8PhWhDRDTmkuVNqcGYromfBBSyvqSYYMByJzS",
    buyer_txn=TransactionWithSigner(txn=buyer_txn, signer= creator.signer),
    transaction_parameters=algokit_utils.TransactionParameters(
            sender=creator.address,
            signer=creator.signer,
            suggested_params=sp
        ),

)

print(f"Called write on {app_client.app_id}")

response = app_client.get_asset_id()

print(response.return_value)


