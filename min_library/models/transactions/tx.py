from typing import Any
from hexbytes import HexBytes

from web3 import Web3, AsyncWeb3
from web3.types import (
    TxReceipt,
    _Hash32,
)

import min_library.models.others.exceptions as exceptions
from min_library.models.others.common import AutoRepr



class Tx(AutoRepr):
    """
    An instance of transaction params for easy execution of actions on it.

    Attributes:
        hash (Optional[_Hash32]): a transaction hash.
        params (Optional[dict]): the transaction parameters.
        receipt (Optional[TxReceipt]): a transaction receipt.
        function_identifier (Optional[str]): a function identifier.
        input_data (Optional[Dict[str, Any]]): an input data.

    """
    hash: _Hash32 | None
    params: dict | None
    receipt: TxReceipt | None
    function_identifier: str | None
    input_data: dict[str, Any] | None

    def __init__(
        self,
        tx_hash: str | _Hash32 | None = None,
        params: dict | None = None
    ) -> None:
        """
        Initialize the class.

        Args:
            tx_hash (Optional[Union[str, _Hash32]]): the transaction hash. (None)
            params (Optional[dict]): a dictionary with transaction parameters. (None)

        """
        if not tx_hash and not params:
            raise exceptions.TransactionException(
                "Specify 'tx_hash' or 'params' argument values!")

        if isinstance(tx_hash, str):
            tx_hash = HexBytes(tx_hash)

        self.hash = tx_hash
        self.params = params
        self.receipt = None
        self.function_identifier = None
        self.input_data = None

    async def wait_for_tx_receipt(
        self,
        web3: Web3 | AsyncWeb3,
        timeout: int | float = 120,
        poll_latency: float = 0.1
    ) -> dict[str, Any]:
        """
        Wait for the transaction receipt.

        Args:
            web3 (Union[Web3, AsyncWeb3]): the Web3 instance.
            timeout (Union[int, float]): the receipt waiting timeout. (120 sec)
            poll_latency (float): the poll latency. (0.1 sec)

        Returns:
            Dict[str, Any]: the transaction receipt.

        """
        self.receipt = dict(await web3.eth.wait_for_transaction_receipt(
            transaction_hash=self.hash, timeout=timeout, poll_latency=poll_latency
        ))

        return self.receipt
