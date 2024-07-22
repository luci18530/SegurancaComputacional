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

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_password = None
    key = None
    decrypted_password = None
    error = None

    if request.method == 'POST' and 'encrypt' in request.form:
        password = request.form['password']
        encrypted_password, key = encrypt_password(password)
        return render_template('index.html', encrypted_password=encrypted_password, key=key.hex())

    if request.method == 'POST' and 'decrypt' in request.form:
        encrypted_password = request.form['encrypted_password']
        key = request.form['key']
        try:
            decrypted_password = decrypt_password(encrypted_password, key)
            return render_template('index.html', decrypted_password=decrypted_password)
        except Exception as e:
            error = "Invalid encrypted password or key"


if __name__ == '__main__':
    app.run(debug=True)
