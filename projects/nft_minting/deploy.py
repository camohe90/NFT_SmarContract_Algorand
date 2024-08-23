from algokit_utils.beta.algorand_client import (
    AlgorandClient,
)
import os
import algokit_utils 

from dotenv import load_dotenv

from smart_contracts.artifacts.nft_minting.nft_minting_client import NftMintingClient

from algosdk.atomic_transaction_composer import TransactionWithSigner


load_dotenv()
PASSPHRASE = os.environ.get("PASSPHRASE")

print("Processing account...")

algorand = AlgorandClient.test_net()
creator = algokit_utils.get_account_from_mnemonic(PASSPHRASE)


app_client = NftMintingClient(
    algod_client = algorand.client.algod,
    sender = creator.address,
    signer= creator.signer,
)

result = app_client.create_bare()

print(f"deploy app with the id {app_client.app_id}")

print(f"and the address {app_client.app_address}")
