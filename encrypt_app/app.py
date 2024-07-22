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



if __name__ == '__main__':
    app.run(debug=True)
