from decimal import Decimal


class TokenAmount:
    """
    A class representing a token amount.

    Attributes:
        Wei (int): The amount in Wei.
        Ether (Decimal): The amount in Ether.
        decimals (int): The number of decimal places.
        GWei (int): The amount in Gwei.

    """
    Wei: int
    Ether: Decimal
    decimals: int
    GWei: int

    def __init__(
        self,
        amount: int | float | Decimal | str,
        decimals: int = 18,
        wei: bool = False,
        set_gwei: bool = False
    ) -> None:
        """
        Initialize the TokenAmount class.

        Args:
            amount (int | float | Decimal | str): The amount.
            decimals (int): The number of decimal places (default is 18).
            wei (bool): If True, the amount is in Wei; otherwise, it's in Ether (default is False).
            set_gwei (bool): If True, the GWei attribute will be calculated and set (default is False).

        """
        if wei:
            self.Wei: int = int(amount)
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

            if set_gwei:
                self.GWei: Decimal = int(amount / 10 ** 9)
        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

            if set_gwei:
                self.GWei: int = int(Decimal(str(amount)) * 10 ** 9)

        self.decimals = decimals

    def __str__(self) -> str:
        """
        Return a string representation of the TokenAmount.

        Returns:
            str: A string representation of the TokenAmount.

        """
        return f'{self.Wei}'
