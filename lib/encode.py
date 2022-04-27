#A short library for encoding floats into a byte array
def float_to_fixed_point(n, fractional_bits=5, max_size= None, min_size= None):
    x = int(round(n * (1 << fractional_bits)))
    n_bytes = (len(bin(x))+5)//8 
    if max_size != None and n_bytes > max_size:
        return bytes([255 for i in range(max_size)])
    if min_size != None and n_bytes < min_size:
        return x.to_bytes((len(bin(x))+5)//8, "little") + bytes([0 for i in range(min_size - n_bytes)])
    return x.to_bytes((len(bin(x))+5)//8, "little") #len(bin(x[])) -2 is bit length

def fixed_point_to_float(n, fractional_bits):
    x = int.from_bytes(n, 'little')
    return x / (1 << fractional_bits)

def byte_array_to_int(b):
    return int.from_bytes(b, "little")
    
def int_to_byte_array(a, n_bytes):
    return a.to_bytes(n_bytes)    