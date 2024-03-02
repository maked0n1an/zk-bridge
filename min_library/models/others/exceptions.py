from typing import Any


class WrongChainId(Exception):
    pass


class WrongCoinSymbol(Exception):
    pass


class ClientException(Exception):
    pass


class InvalidProxy(ClientException):
    pass


class TransactionException(Exception):
    pass


class NetworkNotAdded(Exception):
    pass
