import base64
import os


def extract_from_env(key: str, default_value: object = None) -> str:
    """
    Extracts an environment variable and decrypts it from base64 encoding, with an optional default.

    Args:
        key (str): The environment variable key to extract.
        default_value (object, optional): A default value if the key is not found or decryption fails.
                                           Defaults to None, which returns 'None' or error message.

    Returns:
        str or object: The decrypted value, default value if provided, or error message.
    """
    value = os.getenv(key)
    if value is None:
        return (
            "Environment variable not found."
            if default_value is None
            else default_value
        )
    try:
        return base64.b64decode(value.encode("utf-8")).decode("utf-8")
    except Exception as e:
        return str(e) if default_value is None else default_value
