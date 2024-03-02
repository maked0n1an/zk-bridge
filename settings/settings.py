from typing import (
    List, Optional
)

# Do you want to use wallet names or generate ID's by program?
#   Use own names: True
#   Generate IDs: False
IS_ACCOUNT_NAMES = True

# Do you want to shuffle wallets?
IS_SHUFFLE_WALLETS = True

MINT_NETWORKS: List[List[Optional[str]]] = [
    # ['ethereum', None],
    ['bsc', None],
    ['op_bnb', ],
    ['arbitrum', None],
    ['optimism', None],
    ['polygon', ]
]

IS_SLEEP = True

SLEEP_BETWEEN_MINTS_ON_ONE_ACCOUNT_FROM = 20  # secs
SLEEP_BETWEEN_MINT_ON_ONE_ACCOUNT_TO = 60  # secs

SLEEP_BETWEEN_ACCS_FROM = 100  # secs
SLEEP_BETWEEN_ACCS_TO = 600  # secs

MIN_AMOUNT = 1  # select between MIN_AMOUNT and MAX_AMOUNT
MAX_AMOUNT = 5  # how much NFTs will be claimed on one account

IS_CREATE_LOGS_FOR_EVERY_WALLET = True

# How many retries will be executed if fail?
RETRY_COUNT = 3
