import re

class ChoicesMaxLengthMixin:

    @classmethod
    def max_length(cls):
        """
        Calculate the maximum length needed for storing choice values.
        """
        # Use a generator expression to find the maximum length
        # len(choice.value) gets the length of each choice's value
        # max() finds the largest length among all choices

        return max(len(choice.value) for choice in cls)


def convert_to_lower_case(text):
    if not text or not isinstance(text, str):
        return ""
    
    # Replace common separators with spaces
    text = re.sub(r'[-_]+', ' ', text)
    
    # Handle camelCase by inserting spaces before uppercase letters
    text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
    
    # Split into words and filter out empty strings
    words = [word for word in text.split() if word]
    
    # Convert each word: first letter uppercase, rest lowercase
    lower_words = [word.lower() for word in words]
    
    return ''.join(lower_words)