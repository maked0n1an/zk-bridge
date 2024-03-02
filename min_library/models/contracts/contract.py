from web3 import Web3
from web3.contract import Contract, AsyncContract
from web3.types import TxParams
from eth_typing import ChecksumAddress

from min_library.models.account.account_manager import AccountManager
from min_library.models.others.params_types import ParamsTypes
from min_library.models.others.token_amount import TokenAmount
from min_library.models.transactions.transaction import Transaction


class Contract:
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager
        self.transaction = Transaction(account_manager)

    @staticmethod
    async def get_contract_attributes(
        contract: ParamsTypes.Contract | ParamsTypes.Address
    ) -> tuple[ChecksumAddress, list | None]:
        """
        Get the checksummed contract address and ABI.

        Args:
            contract (ParamsTypes.TokenContract | ParamsTypes.Contract | ParamsTypes.Address):
                The contract address or instance.

        Returns:
            tuple[ChecksumAddress, list | None]: The checksummed contract address and ABI.

        """
        abi = None
        address = None
        if type(contract) in ParamsTypes.Address.__args__:
            address = contract
        else:
            address, abi = contract.address, contract.abi

        return Web3.to_checksum_address(address), abi

    async def get(
        self,
        contract: ParamsTypes.Contract,
        abi: list | str | None = None
    ) -> AsyncContract | Contract:
        """
        Get a contract instance.

        Args:
            contract (ParamsTypes.Contract): the contract address or instance.
            abi (list | str | None, optional): the contract ABI

        Returns:
            AsyncContract | Contract: the contract instance.
        """

        contract_address, contract_abi = await self.get_contract_attributes(
            contract
        )

        if not abi and not contract_abi:
            # todo: сделаем подгрузку abi из эксплорера (в том числе через proxy_address)
            raise ValueError("Can not get contract ABI")
        if not abi:
            abi = contract_abi

        contract = self.account_manager.w3.eth.contract(
            address=contract_address, abi=abi
        )

        return contract

    async def get_decimals(
        self,
        token_contract: ParamsTypes.Contract
    ) -> int:
        decimals = await token_contract.functions.decimals().call()

        return decimals

    def add_multiplier_of_gas(
        self,
        tx_params: TxParams | dict,
        multiplier: float | None = None
    ) -> TxParams | dict:

        tx_params['multiplier'] = multiplier
        return tx_params

    def set_gas_price(
        self,
        gas_price: ParamsTypes.GasPrice,
        tx_params: TxParams | dict,
    ) -> TxParams | dict:
        """
        Set the gas price in the transaction parameters.

        Args:
            gas_price (GWei): The gas price to set.
            tx_params (TxParams | dict): The transaction parameters.

        Returns:
            TxParams | dict: The updated transaction parameters.

        """
        if isinstance(gas_price, float | int):
            gas_price = TokenAmount(
                amount=gas_price,
                decimals=self.account_manager.network.decimals,
                set_gwei=True
            )
        tx_params['gasPrice'] = gas_price.GWei
        return tx_params

    def set_gas_limit(
        self,
        gas_limit: ParamsTypes.GasLimit,
        tx_params: dict | TxParams,
    ) -> dict | TxParams:
        """
        Set the gas limit in the transaction parameters.

        Args:
            gas_limit (int | TokenAmount): The gas limit to set.
            tx_params (dict | TxParams): The transaction parameters.

        Returns:
            dict | TxParams: The updated transaction parameters.

        """
        if isinstance(gas_limit, int):
            gas_limit = TokenAmount(
                amount=gas_limit,
                decimals=self.account_manager.network.decimals,
                wei=True
            )
        tx_params['gas'] = gas_limit.Wei
        return tx_params
