import logging
import random
import requests

from web3 import Web3
from web3.eth import AsyncEth
from web3.middleware import async_geth_poa_middleware
from eth_account.signers.local import LocalAccount
from fake_useragent import UserAgent

from min_library.models.logger.logger import CustomLogger
from min_library.models.network.network import Network
from min_library.models.network.networks import Networks
import min_library.models.others.exceptions as exceptions


class AccountManager:
    network: Network
    account: LocalAccount | None
    w3: Web3

    def __init__(
        self,
        account_id: int | str = None,
        private_key: str | None = None,
        network: Network = Networks.Polygon,
        proxy: str | None = None,
        check_proxy: bool = True,
        create_log_file_per_account: bool = False
    ) -> None:
        self.account_id = account_id
        self.network = network
        self.proxy = proxy
        self._initialize_proxy(check_proxy)
        self._initialize_headers()

        self.w3 = Web3(
            Web3.AsyncHTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'proxy': self.proxy, 'headers': self.headers}
            ),
            modules={'eth': (AsyncEth,)},
            middlewares=[]
        )
        self.w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)

        self._initialize_account(private_key)
        self._initialize_logger(create_log_file_per_account)

    def _initialize_proxy(self, check_proxy: bool):
        if not self.proxy:
            return

        if 'http' not in self.proxy:
            self.proxy = f'http://{self.proxy}'

        if check_proxy:
            your_ip = requests.get(
                url='http://eth0.me',
                proxies={'http': self.proxy, 'https': self.proxy},
                timeout=10
            ).text.rstrip()

            if your_ip not in self.proxy:
                raise exceptions.InvalidProxy(
                    f"Proxy doesn't work! It's IP is {your_ip}"
                )

    def _initialize_headers(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'User-Agent': UserAgent().random
        }

    def _initialize_logger(
        self, 
        create_log_file_per_account: bool
    ) -> None:
        self.custom_logger = CustomLogger(
            account_id=self.account_id,
            address=self.account.address,
            network=self.network.name.capitalize(),
            create_log_file_per_account=create_log_file_per_account
        )

    def _initialize_account(self, private_key: str | None):
        if private_key:
            self.account = self.w3.eth.account.from_key(
                private_key=private_key
            )

        elif private_key == '':
            self.account = None

        else:
            self.account = self.w3.eth.account.create(
                extra_entropy=str(random.randint(1, 999_999_999))
            )
