import struct

def float_list_to_bytes(float_list):
    """
    Converts a list of floating-point numbers into a byte array.

    Args:
        float_list (list of float): A list of floating-point numbers to be converted.

    Returns:
        bytes: A byte array representing the floating-point numbers packed in binary format.
    """
    return struct.pack('f' * len(float_list), *float_list)
