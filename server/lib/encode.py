#A short library for encoding floats into a byte array
def float_to_fixed_point(n : float, fractional_bits : int = 5, max_size : int = None) -> bytes:
    x = int(round(n * (1 << fractional_bits)))
    byte_array = x.to_bytes((len(bin(x))+5)//8, "little")
    if max_size != None and (len(bin(x))+5)//8 > max_size:
        return bytes([255 for i in range(max_size)])
    return x.to_bytes((len(bin(x))+5)//8, "little") #len(bin(x)) -2 is bit length

def fixed_point_to_float(n: bytes, fractional_bits: int) -> float:
    x = int.from_bytes(n, 'little')
    return x / (1 << fractional_bits)