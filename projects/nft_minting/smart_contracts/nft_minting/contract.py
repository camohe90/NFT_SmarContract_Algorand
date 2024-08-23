from algopy import ARC4Contract, String, Bytes, itxn, UInt64, gtxn
from algopy.arc4 import abimethod


class NftMinting(ARC4Contract):

    asset_created: UInt64

    @abimethod()
    def mint_nft(self,
                 asset_name: String,
                 unit_name: String,
                 url: String,
                 metadata_hash: Bytes,
                 buyer_txn: gtxn.PaymentTransaction
                 ) -> None:
    
        self.asset_created = itxn.AssetConfig (
            asset_name= asset_name,
            unit_name= unit_name,
            total= 1,
            decimals= 0,
            url= url,
            metadata_hash= metadata_hash
        ).submit().created_asset.id

    @abimethod
    def get_asset_id(self)-> UInt64:
        return self.asset_created
