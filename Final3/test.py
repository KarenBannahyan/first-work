from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def hash_text(plain_text):

    key = os.urandom(32)
    iv = os.urandom(16)

    # Шифрование текста
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padding_length = 16 - len(plain_text) % 16
    padded_text = plain_text + chr(padding_length) * padding_length

    encrypted_text = encryptor.update(padded_text.encode()) + encryptor.finalize()

    return base64.b64encode(encrypted_text).decode('utf-8'), base64.b64encode(key).decode('utf-8'), base64.b64encode(iv).decode('utf-8')

def unhash_text(encrypted_text_b64, key_b64, iv_b64):
    encrypted_text = base64.b64decode(encrypted_text_b64)
    key = base64.b64decode(key_b64)
    iv = base64.b64decode(iv_b64)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()

    padding_length = decrypted_text[-1]
    decrypted_text = decrypted_text[:-padding_length].decode('utf-8')

    return decrypted_text

encrypted_text = input("Введите зашифрованный текст (в формате base64): ")
key = input("Введите ключ (в формате base64): ")
iv = input("Введите IV (в формате base64): ")

decrypted_text = unhash_text(encrypted_text, key, iv)

print("Decrypted text:", decrypted_text)
