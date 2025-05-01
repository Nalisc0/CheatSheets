#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256, MD5

def aes_encrypt(plaintext, key, iv) -> bytes:
    """Chiffre un fichier avec AES-CBC et padding PKCS7"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def aes_decrypt(ciphertext, key, iv) -> bytes:
    """Déchiffre un fichier avec AES-CBC et padding PKCS7"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    return plaintext


def hash_sha256_bytes(plaintext) -> bytes:
    """Hash SHA256. Retourne les bytes"""
    h = SHA256.new()
    h.update(plaintext)
    return h.digest()

def hash_sha256_hex(plaintext) -> str:
    """Hash SHA256. Retourne une string hexadécimale"""
    h = SHA256.new()
    h.update(plaintext)
    return h.hexdigest()

def hash_md5_bytes(plaintext) -> bytes:
    """Hash MD5. Retourne les bytes"""
    h = MD5.new()
    h.update(plaintext)
    return h.digest()

def hash_md5_hex(plaintext) -> str:
    """Hash MD-. Retourne une string hexadécimale"""
    h = MD5.new()
    h.update(plaintext)
    return h.hexdigest()