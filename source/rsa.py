import random
from math import gcd
from sympy import isprime
import hashlib

class RSA:
    def __init__(self, key_size: int, mouse_data: list[tuple]):
        self.key_size = key_size
        self.e = 65537  # Standard offentlig eksponent
        self.d = None
        self.n = None
        self._generate_keys(mouse_data)

    @staticmethod
    def _generate_seed(mouse_data: list[tuple]) -> int: # _ = private metode
        # SHA-256 hasher hele listen direkte til ét konsistent tal
        return int.from_bytes(hashlib.sha256(str(mouse_data).encode()).digest(), 'big')

    @staticmethod
    def _generate_prime(bits: int) -> int: # _ = private metode
        # Genererer ulige kandidat og tjekker om det er et primtal via sympy
        while True:
            candidate = random.getrandbits(bits) | (1 << bits - 1) | 1
            if isprime(candidate):
                return candidate

    def _generate_keys(self, mouse_data: list[tuple]) -> None: # _ = private metode
        # Samme seed = samme nøgler hver gang
        random.seed(self._generate_seed(mouse_data))
        half = self.key_size // 2

        while True:
            p = self._generate_prime(half)
            q = self._generate_prime(half)
            while q == p:
                q = self._generate_prime(half)

            phi_n = (p - 1) * (q - 1)
            if gcd(self.e, phi_n) == 1:
                break

        self.n = p * q
        self.d = pow(self.e, -1, phi_n)  # e*d ≡ 1 (mod phi(n))

    # @property gør at man skriver rsa.public_key i stedet for rsa.public_key()
    # nøglen er en egenskab ved objektet, ikke en handling man udfører
    @property
    def public_key(self) -> dict:
        return {'e': self.e, 'n': self.n}

    @property
    def private_key(self) -> dict:
        # d må aldrig deles
        return {'d': self.d, 'n': self.n}

    def encrypt(self, message: bytes | str) -> list[dict]:
        if isinstance(message, str):
            message = message.encode('utf-8')

        max_bytes = (self.n.bit_length() - 1) // 8
        chunks = []
        for i in range(0, len(message), max_bytes):
            chunk = message[i:i + max_bytes]
            # c = m^e mod n
            chunks.append({'c': pow(int.from_bytes(chunk, 'big'), self.e, self.n), 'len': len(chunk)})
        return chunks

    def decrypt(self, chunks: list) -> str:
        decrypted = bytearray()
        for item in chunks:
            c      = item.get('c') if isinstance(item, dict) else item
            length = item.get('len') if isinstance(item, dict) else None
            dec    = pow(c, self.d, self.n)  # m = c^d mod n

            length = length or (dec.bit_length() + 7) // 8
            decrypted.extend(dec.to_bytes(length, 'big'))

        try:
            return decrypted.decode('utf-8')
        except Exception:
            # Hvis UTF-8 dekodning fejler returneres rå bytes
            return bytes(decrypted)