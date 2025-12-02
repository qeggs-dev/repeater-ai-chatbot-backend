def str_to_bool(s: str):
    """
    Convert a string to a boolean value.

    Parameters:
    s (str): The string to convert.

    Returns:
    bool: The boolean value of the string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    if s.lower() in ["true", "yes", "1", "t", "y", "on"]:
        return True
    elif s.lower() in ["false", "no", "0", "f", "n", "off"]:
        return False
    else:
        raise ValueError("Cannot convert string to boolean.")