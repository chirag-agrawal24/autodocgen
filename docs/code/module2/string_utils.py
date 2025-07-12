def greet(name):
    """Returns a personalized greeting string for a given name."""
    return f'Hello, {name}!'


def capitalize_words(text):
    """Returns a new string with each word in the input text capitalized."""
    return ' '.join(word.capitalize() for word in text.split())


def count_words(text):
    """Counts the number of words in a given text string."""
    return len(text.split())
