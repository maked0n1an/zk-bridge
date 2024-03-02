from web3.types import TxParams

from min_library.models.client import Client
from min_library.models.network.networks import Networks
from min_library.models.others.constants import LogStatus
from min_library.models.others.token_amount import TokenAmount


class ZkBridge:
    MINT_DATA_DICT = {
        "Polyhedra 2024": {
            'networks': {
                Networks.Arbitrum.name: '0x5d340658400e1d2352262c7c361ace0366bf6c24',
                Networks.Bsc.name:      '0x7c3aa07721578d00babdebf17c3352d7658b67fd',
                Networks.Ethereum.name: '0xb7545014a3973b0d27a65ee76d1a5ee29d37b1c9',
                Networks.Op_bnb.name:    '0x61d7e121185b1d7902a3da7f3c8ac9faaee8863b',
                Networks.Optimism.name: '0xee7c3d2ff9ef8dbf3e66704a156d3ee9700cf72e',
                Networks.Polygon.name:  '0xCd4b2E538c9D2C1ca117C8f5f2E8Fa56f6bA1069'
            },
            'data': '0x1249c58b'
        }
    }

    GAS_PRICE_DICT = {
        Networks.Bsc.name: 1,
        Networks.Op_bnb.name: 0.00002,
    }

    def __init__(
        self,
        client: Client
    ) -> None:
        self.client = client

    async def mint(
        self,
        nft_name: str,
        network: str,
    ) -> bool:
        try:
            mint_contract, _ = await (
                self.client.contract.get_contract_attributes(
                    contract=self.MINT_DATA_DICT[nft_name]['networks'][network]
                )
            )

            tx_params = TxParams(
                to=mint_contract,
                data=self.MINT_DATA_DICT[nft_name]['data']
            )

            if network in self.GAS_PRICE_DICT:
                gas_price = TokenAmount(
                    amount=self.GAS_PRICE_DICT[network],
                    decimals=self.client.account_manager.network.decimals,
                    set_gwei=True
                )
                tx_params['gasPrice'] = gas_price.GWei

            tx = await self.client.contract.transaction.sign_and_send(
                tx_params=tx_params
            )

            receipt = await tx.wait_for_tx_receipt(
                web3=self.client.account_manager.w3
            )

            if receipt:
                account_network = self.client.account_manager.network
                full_path = account_network.explorer + account_network.TX_PATH
                self.client.account_manager.custom_logger.log_message(
                    level=LogStatus.MINTED,
                    message=(
                        f'The "Polyhedra 2024" NFT has been minted: '
                        f'{full_path + tx.hash.hex()}'
                    )
                )
                return True
        except Exception as e:
            self.client.account_manager.custom_logger.log_message(
                level=LogStatus.ERROR,
                message=e
            )

        return False
