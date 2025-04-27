class ChoicesMaxLengthMixin:

    @classmethod
    def max_length(cls):
        return max(len(choice.value) for choice in cls)
