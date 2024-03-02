import asyncio
import json
import random
from pathlib import Path
from min_library.models.logger.logger import ConsoleLoggerSingleton

from settings.settings import (
    RETRY_COUNT,
    SLEEP_BETWEEN_ACCS_FROM,
    SLEEP_BETWEEN_ACCS_TO
)


def read_txt(filepath: Path | str):
    with open(filepath, 'r') as file:
        return [row.strip() for row in file]


def load_json(filepath: Path | str):
    with open(filepath, 'r') as file:
        return json.load(file)


def format_output(message: str):
    print(f"{message:^80}")


def retry(func):
    async def _wrapper(*args, **kwargs):
        retries = 1

        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)

                return result
            except Exception as e:
                await delay(10, 60, f"One more retry: {retries}/{RETRY_COUNT}")
                retries += 1

    return _wrapper


async def delay(
    sleep_from: int = SLEEP_BETWEEN_ACCS_FROM,
    sleep_to: int = SLEEP_BETWEEN_ACCS_TO,
    message: str = ""
) -> None:

    delay_secs = random.randint(sleep_from, sleep_to)
    
    logger = ConsoleLoggerSingleton.get_logger()
    logger.info(f"Sleeping for {delay_secs} seconds: {message}")

    await asyncio.sleep(delay_secs)
