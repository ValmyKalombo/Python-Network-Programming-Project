from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, binascii

key = AESGCM.generate_key(bit_length=256)
print("Your AES key (raw bytes):", key)
print("Your AES key (hex):", binascii.hexlify(key).decode())