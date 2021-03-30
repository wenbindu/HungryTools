import re


def hex_to_char(hex_str):
    """ converts a single hex-encoded character 'FFFF' into the corresponding real character """
    return chr(int(hex_str, 16))

def parser_hex(hex_str):
    """converts a hex-encoded character '%u****' into the real character string.

    Args:
        hex_str (str): string contains the %u
    """

    percent_u = re.compile(r"%u([0-9a-fA-F]{4})")
    decoded = percent_u.sub(lambda m: hex_to_char(m.group(1)), hex_str)

    return decoded
