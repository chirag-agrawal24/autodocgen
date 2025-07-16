def greet(name):
    """Returns a greeting string for the given name."""
    return f'Hello, {name}!'


def capitalize_words(text):
    """Capitalizes the first letter of each word in the given text.

 Args:
     text (str): The input text to be modified.

 Returns:
     str: The text with the first letter of each word capitalized."""
    return ' '.join(word.capitalize() for word in text.split())


def count_words(text):
    """Counts the number of words in the input text."""
    return len(text.split())
