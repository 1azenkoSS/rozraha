from flask import Flask, request, jsonify
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

def aes_encrypt(plaintext, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded_text = pad(plaintext.encode(), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return binascii.hexlify(encrypted_text).decode()

def aes_decrypt(ciphertext, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(binascii.unhexlify(ciphertext)), AES.block_size)
    return decrypted_text.decode()

@app.route('/encrypt', methods=['POST'])
def encrypt_endpoint():
    data = request.json
    plaintext = data.get('plaintext')
    key = data.get('key')

    if len(key) != 16:  # Key must be 16 characters long
        return jsonify({"error": "Key must be 16 characters long."}), 400
    if not plaintext or not key:
        return jsonify({"error": "Please provide both plaintext and key."}), 400

    try:
        encrypted_text = aes_encrypt(plaintext, key)
        return jsonify({"ciphertext": encrypted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_endpoint():
    data = request.json
    ciphertext = data.get('ciphertext')
    key = data.get('key')

    if len(key) != 16:  # Key must be 16 characters long
        return jsonify({"error": "Key must be 16 characters long."}), 400
    if not ciphertext or not key:
        return jsonify({"error": "Please provide both ciphertext and key."}), 400

    try:
        decrypted_text = aes_decrypt(ciphertext, key)
        return jsonify({"plaintext": decrypted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
