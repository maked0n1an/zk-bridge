from min_library.models.network.network import Network
from min_library.models.others.constants import TokenSymbol
from min_library.models.others.common import Singleton

import min_library.models.others.exceptions as exceptions


class Networks(metaclass=Singleton):
    # Mainnet
    Ethereum = Network(
        name='ethereum',
        rpc='https://rpc.ankr.com/eth/720840b6beda865781b7beb539459137b7da7a657a58524b341d980a0a510f48',
        chain_id=1,
        tx_type=2,
        coin_symbol=TokenSymbol.ETH,
        decimals=18,
        explorer='https://etherscan.io',
    )

    Arbitrum = Network(
        name='arbitrum',
        rpc=[
            'https://rpc.ankr.com/arbitrum/720840b6beda865781b7beb539459137b7da7a657a58524b341d980a0a510f48',
            'https://rpc.ankr.com/arbitrum/a711c35e9e092e57fed201c2960689957eaf1ad37b7e7ec4eca11accd776e5a9'
        ],
        chain_id=42161,
        tx_type=2,
        coin_symbol=TokenSymbol.ETH,
        decimals=18,
        explorer='https://arbiscan.io'
    )
    
    Bsc = Network(
        name='bsc',
        rpc='https://rpc.ankr.com/bsc',
        chain_id=56,
        tx_type=0,
        coin_symbol=TokenSymbol.BNB,
        decimals=18,
        explorer='https://bscscan.com'
    )

    Optimism = Network(
        name='optimism',
        rpc='https://rpc.ankr.com/optimism',
        chain_id=10,
        tx_type=2,
        coin_symbol=TokenSymbol.ETH,
        decimals=18,
        explorer='https://optimistic.etherscan.io',
    )
    
    Op_bnb = Network(
        name='op_bnb',
        rpc=[
            "https://opbnb-mainnet-rpc.bnbchain.org",
            "https://opbnb-mainnet.nodereal.io/v1/64a9df0874fb4a93b9d0a3849de012d3",
            "https://opbnb-mainnet.nodereal.io/v1/e9a36765eb8a40b9bd12e680a1fd2bc5",
            "https://opbnb-rpc.publicnode.com",
        ],
        chain_id=204,
        tx_type=0,
        coin_symbol=TokenSymbol.BNB,
        decimals=18,
        explorer="https://mainnet.opbnbscan.com",
    )
    
    Polygon = Network(
        name='polygon',
        rpc='https://rpc.ankr.com/polygon',
        chain_id=137,
        tx_type=2,
        coin_symbol=TokenSymbol.MATIC,
        decimals=18,
        explorer='https://polygonscan.com',
    )

    @classmethod
    def get_network(
        cls, 
        network_name: str,
    ) -> Network:
        network_name = network_name.capitalize()

        if not hasattr(cls, network_name):
            raise exceptions.NetworkNotAdded(
                f"The {network_name} network has not been added to {__class__.__name__} class"
            )

        return getattr(cls, network_name)