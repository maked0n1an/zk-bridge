import json

from web3 import (
    Web3,
    types
)
from typing import Any
from eth_typing import ChecksumAddress

from min_library.models.others.common import AutoRepr


class RawContract(AutoRepr):
    """
    An instance of a raw contract.

    Attributes:
        title (str): a contract title.
        address (ChecksumAddress): a contract address.
        abi (list[dict[str, Any]] | str): an ABI of the contract.
        is_native_token (bool): is this contract native token of network (False)

    """
    title: str
    address: ChecksumAddress
    abi: list[dict[str, Any]]

    def __init__(
        self,
        title: str,
        address: str | types.Address | types.ChecksumAddress | types.ENS,
        abi: list[dict[str, Any]] | str
    ) -> None:
        """
        Initialize the class.

        Args:
            title (str): a contract title.
            address (str): a contract address.
            abi (Union[List[Dict[str, Any]], str]): an ABI of the contract.
            is_native_token (bool): is this contract native token of network (False)
        """
        self.title = title
        self.address = Web3.to_checksum_address(address)
        self.abi = json.loads(abi) if isinstance(abi, str) else abi
