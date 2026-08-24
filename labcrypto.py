# labcrypto.py
# A TOY stand-in for real encryption, used ONLY to show the concept.
# It is NOT secure. Real systems (and HTTPS/TLS) use vetted, modern encryption.
# Here we just XOR the message with a shared secret so it becomes scrambled
# bytes that the attacker cannot read or safely change without the key.

SECRET_KEY = b"lab-shared-secret"   # the bank and the customer both know this; the attacker does NOT


def scramble(data: bytes) -> bytes:
    """Turn readable bytes into scrambled bytes using the shared key."""
    return bytes(b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(data))


def unscramble(data: bytes) -> bytes:
    """Reverse scramble(): XOR with the same key returns the original bytes."""
    return scramble(data)
