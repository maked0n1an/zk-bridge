import asyncio
import random
import sys
import time
from questionary import (
    questionary,
    Choice
)
from min_library.models.logger.logger import ConsoleLoggerSingleton

from min_library.utils.config import (
    ACCOUNT_NAMES,
    PRIVATE_KEYS
)
from min_library.utils.helpers import (
    delay,
    format_output
)
from settings.modules_settings import mint_polyhedra_2024_nft

from settings.settings import (
    IS_ACCOUNT_NAMES,
    IS_SHUFFLE_WALLETS,
    IS_SLEEP
)


def greetings():
    name_label = "========= zkBridge Minter Software ========="
    brand_label = "========== Author: M A K E D 0 N 1 A N =========="
    telegram = "======== https://t.me/crypto_maked0n1an ========"

    print("")
    format_output(name_label)
    format_output(brand_label)
    format_output(telegram)


def end_of_work():
    exit_label = "========= The bot has ended it's work! ========="
    format_output(exit_label)
    sys.exit()


def is_bot_setuped_to_start():
    end_bot = False

    if len(PRIVATE_KEYS) == 0:
        print("Don't imported private keys in 'private_keys.txt'!")
        return end_bot
    if len(ACCOUNT_NAMES) == 0 and IS_ACCOUNT_NAMES:
        print("Please insert names into account_names.txt")
        return end_bot
    if len(PRIVATE_KEYS) != len(ACCOUNT_NAMES) and IS_ACCOUNT_NAMES:
        print(
            "The account names' amount must be equal to private keys' amount"
        )
        return end_bot

    return True


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice(
                "1) Mint 'Polyhedra 2024 NFT' on one or some chains configured in settings",
                mint_polyhedra_2024_nft
            ),
            Choice("2) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        exit_label = "========= Exited ========="
        format_output(exit_label)
        sys.exit()

    return result


def get_accounts():
    if IS_ACCOUNT_NAMES:
        accounts = [
            {
                "name": account_name,
                "key": key
            } for account_name, key in zip(ACCOUNT_NAMES, PRIVATE_KEYS)
        ]
    else:
        accounts = [
            {
                "name": _id,
                "key": key
            } for _id, key in enumerate(PRIVATE_KEYS, start=1)
        ]

    return accounts


async def run_module(module, wallet):
    return await module(wallet["name"], wallet["key"])


def measure_time_for_all_work(start_time: float):
    end_time = round(time.time() - start_time, 2)
    seconds = round(end_time % 60, 2)
    minutes = round(end_time / 60, 1) if end_time > 60 else 0
    hours = end_time / 3600 if end_time > 3600 else 0

    logger.log(
        20, 
        (
            f"The bot has ended it's work with work time: "
            f"{hours} hours {minutes} minutes {seconds} seconds" 
        )
    )


async def main(module):
    accounts = get_accounts()

    if IS_SHUFFLE_WALLETS:
        random.shuffle(accounts)

    for account in accounts:
        is_result = await run_module(module, account)

        if IS_SLEEP and account != accounts[-1] and is_result:
            await delay(message='before next account')

if __name__ == '__main__':
    greetings()

    if not is_bot_setuped_to_start():
        exit_label = "========= The bot has ended it's work! ========="
        format_output(exit_label)
        sys.exit()

    module_data = get_module()

    start_time = time.time()
    logger = ConsoleLoggerSingleton.get_logger()
    logger.log(
        20, "The bot started to measure time for all work"
    )

    asyncio.run(main(module_data))

    measure_time_for_all_work(start_time)
