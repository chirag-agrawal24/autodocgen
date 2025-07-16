def greet(name):
    """Returns a personalized greeting string for a given name."""
    return f'Hello, {name}!'


def capitalize_words(text):
    """Capitalizes the first letter of each word in the input text and returns the modified string."""
    return ' '.join(word.capitalize() for word in text.split())


def count_words(text):
    """Count the number of words in the given text.

 
Parameters
----------
text : str
    The input text.

Returns
-------
int
    The number of words in the text."""
    return len(text.split())
