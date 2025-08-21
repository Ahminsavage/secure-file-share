import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from config import FILE_KMS_KEK

def encrypt_file(file_data: bytes):
    # Generate random 32-byte AES key for file
    file_key = get_random_bytes(32)

    # AES-GCM encryption
    cipher = AES.new(file_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)

    # Wrap file key using KEK (AES-ECB)
    kek_cipher = AES.new(FILE_KMS_KEK, AES.MODE_ECB)
    wrapped_key = kek_cipher.encrypt(file_key)

    return {
        "ciphertext": ciphertext,
        "nonce": cipher.nonce,
        "tag": tag,
        "wrapped_key": wrapped_key
    }

def decrypt_file(ciphertext: bytes, nonce: bytes, tag: bytes, wrapped_key: bytes):
    # Unwrap key
    kek_cipher = AES.new(FILE_KMS_KEK, AES.MODE_ECB)
    file_key = kek_cipher.decrypt(wrapped_key)

    # AES-GCM decryption
    cipher = AES.new(file_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext
