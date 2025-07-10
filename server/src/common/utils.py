from typing import Type, Any


class ChoicesMaxLengthMixin:
    @classmethod
    def max_length(
        cls: Type[Any],
    ) -> int:
        return max(len(choice.value) for choice in cls)
