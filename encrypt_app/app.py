from flask import Flask, render_template, request
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__)

# Função para encriptografar a senha
def encrypt_password(password):
    key = os.urandom(16)  # Gera uma chave aleatória de 16 bytes
    cipher = AES.new(key, AES.MODE_EAX)  # Modo de operação EAX para AES
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8'), key

# Função para desencriptografar a senha
def decrypt_password(encrypted_password, key_hex):
    key = bytes.fromhex(key_hex)
    encrypted_data = base64.b64decode(encrypted_password)
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    password = cipher.decrypt(ciphertext).decode('utf-8')
    return password




if __name__ == '__main__':
    app.run(debug=True)
