from machine import rng

def rand_byte():
    return rng() >> 16

def randint_32():
    r1 = rng()
    r2 = rng()
    return int((r1 << 8) + (r2 >> 16))