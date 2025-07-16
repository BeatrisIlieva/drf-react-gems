from typing import Type, Any


class ChoicesMaxLengthMixin:

    @classmethod
    def max_length(cls: Type[Any]) -> int:
        """
        Calculate the maximum length needed for storing choice values.
        """
        # Use a generator expression to find the maximum length
        # len(choice.value) gets the length of each choice's value
        # max() finds the largest length among all choices
        return max(len(choice.value) for choice in cls)
