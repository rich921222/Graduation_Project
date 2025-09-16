from xxhash import xxh32
import numpy as np

def hashB(npArray,bits):
    return np.mod(xxh32(npArray.tobytes()).intdigest(), 2**bits)