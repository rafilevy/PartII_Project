#A short library for encoding floats into a byte array
def float_to_fixed_point(n : float, fractional_bits: int) -> bytes:
    x = int(round(n * (1 << fractional_bits)))
    return x.to_bytes((len(bin(x))+5)//8, "little") #len(bin(x)) -2 is bit length

def fixed_point_to_float(n: bytes, fractional_bits: int) -> float:
    x = int.from_bytes(n, 'little')
    return x / (1 << fractional_bits)