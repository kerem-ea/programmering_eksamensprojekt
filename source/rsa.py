import random
from sympy import randprime
from math import gcd

def generate_seed_from_mouse(mouse_data):
    """
    mouse_data: liste af tuples (dx, dy, dt)
    Returnerer en simpel int seed
    """
    seed = 0
    for dx, dy, dt in mouse_data:
        # Simpel XOR af forskudte bits
        seed ^= (dx << 32) ^ (dy << 16) ^ dt
    return seed

def RSA_KEYGEN_with_seed(key_size, mouse_data):
    seed = generate_seed_from_mouse(mouse_data)
    random.seed(seed)  # Seed Python's random så randprime bliver deterministisk
    half_key_size = key_size // 2
    e = 65537

    while True:
        p = randprime(2 ** (half_key_size - 1), 2 ** half_key_size)
        q = randprime(2 ** (half_key_size - 1), 2 ** half_key_size)
        while q == p:
            q = randprime(2 ** (half_key_size - 1), 2 ** half_key_size)

        n = p * q
        phi_n = (p - 1) * (q - 1)

        if gcd(e, phi_n) == 1:
            break

    d = pow(e, -1, phi_n)
    return {'e': e, 'd': d, 'n': n}

def RSA_ENCRYPT(message: bytes | str, public_key):
    e, n = public_key['e'], public_key['n']
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message

    # Antal bytes vi kan kryptere per chunk: sikre at chunk_int < n
    max_bytes = (n.bit_length() - 1) // 8
    if max_bytes <= 0:
        raise ValueError("Public modulus too small to encrypt any bytes")

    encrypted_chunks = []
    for i in range(0, len(message_bytes), max_bytes):
        chunk = message_bytes[i:i + max_bytes]
        chunk_int = int.from_bytes(chunk, 'big')
        cipher_int = pow(chunk_int, e, n)
        encrypted_chunks.append({'c': cipher_int, 'len': len(chunk)})

    return encrypted_chunks


def RSA_DECRYPT(encrypted_chunks, private_key) -> str:
    d, n = private_key['d'], private_key['n']
    decrypted = bytearray()

    for item in encrypted_chunks:
        # Accepterer både dict-objekter og simple ints
        if isinstance(item, dict):
            c = item.get('c')
            length = item.get('len', 0)
        else:
            c = item
            length = None

        dec_int = pow(c, d, n)

        if length is None:
            length = (dec_int.bit_length() + 7) // 8

        if length > 0:
            decrypted.extend(dec_int.to_bytes(length, 'big'))

    try:
        return decrypted.decode('utf-8')
    except Exception:
        # Hvis dekodning fejler, returner rå bytes
        return bytes(decrypted)