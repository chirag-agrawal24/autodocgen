def greet(name):
    """Returns a greeting string for the given name."""
    return f"Hello, {name}!"

def capitalize_words(text):
    return " ".join(word.capitalize() for word in text.split())

def count_words(text):
    """Counts the number of words in the input text."""
    return len(text.split())
