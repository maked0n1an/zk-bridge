import asyncio
import logging
import random
import sys

from min_library.models.account.account_manager import AccountManager
from min_library.models.contracts.contract import Contract
from min_library.models.network.network import Network
from min_library.models.network.networks import Networks
from settings.settings import (
    SLEEP_BETWEEN_ACCS_FROM, 
    SLEEP_BETWEEN_ACCS_TO
)


class Client:
    def __init__(
        self,
        account_id: str | int,
        private_key: str | None = None,
        network: Network = Networks.Polygon,
        proxy: str | None = None,
        check_proxy: bool = True,
        create_log_file_per_account: bool = False
    ) -> None:
        self.account_manager = AccountManager(
            account_id=account_id,
            private_key=private_key,
            network=network,
            proxy=proxy,
            check_proxy=check_proxy,
            create_log_file_per_account=create_log_file_per_account
        )

        self.contract = Contract(account_manager=self.account_manager)
    
    async def initial_delay(
        self,
        sleep_from:int = SLEEP_BETWEEN_ACCS_FROM, 
        sleep_to :int = SLEEP_BETWEEN_ACCS_TO,
        message: str = 'before next step'
    ) -> None:
        delay = random.randint(sleep_from, sleep_to)
        
        self.account_manager.custom_logger.log_message(
            "INFO", f"Sleeping {delay} secs {message}"
        )
        await asyncio.sleep(delay)