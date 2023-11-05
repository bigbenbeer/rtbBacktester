from enum import Enum

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def devList(cls, num_indicators=5):
        """Returns a list of the first `num_indicators` members of the enum.

        Args:
            num_indicators (int): The number of members to return.

        Returns:
            list: A list of enum members.
        """
        if not isinstance(num_indicators, int):
            raise TypeError("num_indicators must be an integer.")

        if num_indicators < 1:
            raise ValueError(
                "num_indicators must be greater than or equal to 1.")

        return list(map(lambda c: c.value, cls))[:num_indicators]
