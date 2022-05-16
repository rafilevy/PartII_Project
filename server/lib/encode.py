from struct import pack, unpack
def float_to_byte_array(n):
    return pack("<f", n)

def byte_array_to_float(byte_array):
    return unpack("<f", byte_array)


def float_to_int(n):
    return byte_array_to_int(float_to_byte_array(n))
def int_to_float(n):
    return byte_array_to_float(int_to_byte_array(n))


def int_to_byte_array(n, signed=True):
    if signed:
        fmt = "<i"
    else:
        fmt = "<I"
    return pack(fmt, n)

def byte_array_to_int(byte_array, signed=True):
    if signed:
        fmt = "<i"
    else:
        fmt = "<I"
    return unpack(fmt, byte_array)