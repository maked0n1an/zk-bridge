from typing import (
    List, Optional
)

# Do you want to use wallet names or generate ID's by program?
#   Use own names: True
#   Generate IDs: False
IS_ACCOUNT_NAMES = True

# Do you want to shuffle wallets?
IS_SHUFFLE_WALLETS = True

# If you want mint in selected network so set it in MINT_NETWORKS like:
# - with 100% chance of executing:
#   ['bsc',],
# - with 50% chance of executing, so set it like:
#   ['bsc', None],
# - with 33% chance of executing, so set it like:
#   ['bsc', 'None', None],
# - mixing another networks:
#   [None, 'bsc', 'arbitrum'],
# - maybe such option:
#   ['bsc', 'op_bnb', 'arbitrum', 'optimism', 'polygon', None],
# You can comment or uncomment the row you need. 
# If you want to mint ONLY in one network (for example, 'bsc')
# with guaranteed mint, please set it like:
#
# MINT_NETWORKS: List[List[Optional[str]]] = [
#     # ['ethereum', None],
#     ['bsc', ],
#     #['op_bnb', ],
#     #['arbitrum', None],
#     #['optimism', None],
#     #['polygon', ]
# ]
# Available networks:
# 'ethereum' | 'bsc' | 'op_bnb' | 'arbitrum' | 'optimism' | 'polygon'

MINT_NETWORKS: List[List[Optional[str]]] = [
    # ['ethereum', None],
    ['bsc', None],
    ['op_bnb', ],
    ['arbitrum', 'optimism', None],
    # ['polygon', ]
]

IS_SLEEP = True

SLEEP_BETWEEN_MINTS_ON_ONE_ACCOUNT_FROM = 20  # secs
SLEEP_BETWEEN_MINT_ON_ONE_ACCOUNT_TO = 60  # secs

SLEEP_BETWEEN_ACCS_FROM = 100  # secs
SLEEP_BETWEEN_ACCS_TO = 600  # secs

# Do you want to create log file for every wallet? Yes - True, No - False
IS_CREATE_LOGS_FOR_EVERY_WALLET = False

# (not working now) How many retries will be executed if fail?
RETRY_COUNT = 3
