import random
from min_library.models.client import Client
from min_library.models.network.networks import Networks
from settings.settings import (
    IS_CREATE_LOGS_FOR_EVERY_WALLET,
    IS_SLEEP,
    MINT_NETWORKS,
    SLEEP_BETWEEN_MINT_ON_ONE_ACCOUNT_TO,
    SLEEP_BETWEEN_MINTS_ON_ONE_ACCOUNT_FROM
)
from tasks.zk_bridge import ZkBridge


async def mint_polyhedra_2024_nft(account_id, private_key) -> bool:
    await _mint_one_nft_or_some_nfts(account_id, private_key, "Polyhedra 2024")

## -------------------- DONT TOUCH IT ----------------------
async def _mint_one_nft_or_some_nfts(account_id, private_key, nft_name) -> bool:
    random.shuffle(MINT_NETWORKS)
    has_minted_one_time = False

    for option in MINT_NETWORKS:
        network_name = random.choice(option)
        if network_name is None:
            continue

        network_object = Networks.get_network(network_name=network_name)
        client = Client(
            account_id=account_id,
            private_key=private_key,
            network=network_object,
            create_log_file_per_account=IS_CREATE_LOGS_FOR_EVERY_WALLET
        )
        zkbridge = ZkBridge(client)

        network = client.account_manager.network.name
        is_result = await zkbridge.mint(
            nft_name=nft_name,
            network=network
        )

        if IS_SLEEP and network != MINT_NETWORKS[-1] and is_result:
            has_minted_one_time = is_result
            await client.initial_delay(
                sleep_from=SLEEP_BETWEEN_MINTS_ON_ONE_ACCOUNT_FROM,
                sleep_to=SLEEP_BETWEEN_MINT_ON_ONE_ACCOUNT_TO,
                message='before next mint'
            )

    return has_minted_one_time
