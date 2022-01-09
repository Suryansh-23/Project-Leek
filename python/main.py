from Algorithms import aes_encrypt, aes_decrypt, stegano_encrypt, stegano_decrypt

from random import choices
from string import ascii_letters, digits

from flask import Flask
from flask import jsonify, request


AUTH = ""  # AUTH (global var) for maintaining a valid Auth-Key to be used to verify connection with authenticated clients only


def random_key(k: int = 16):
    """Generates a random auth key"""
    # encrypt_type is 0 for 128 bit, 1 for 192 bit, 2 for 256 bit
    str_pool = ascii_letters + digits
    return "".join(choices(str_pool, k=k))


def str2hex(s: str):
    return "0x" + "".join([hex(ord(i)).lstrip("0x") for i in s])


def hex2str(hex: str):
    hex = hex[2:]
    chrs = [hex[i : i + 2] for i in range(0, len(hex), 2)]
    s = ""
    for i in chrs:
        n = int(f"0x{i}", 16)
        if n >= 32:
            s += chr(n)
    return s


app = Flask(__name__)


@app.route("/")
def home():
    """Standard API Route for Testing if API is online"""
    return "RESTFul API for Project Leɘk"


@app.route("/cipher_key", methods=["GET"])
def cipher_key():
    try:
        encrypt_type = int(request.headers.get("Encryption-Type"))
    except:
        return jsonify(False), 500
    # encrypt_type is 0 for 128 bit, 1 for 192 bit, 2 for 256 bit
    if encrypt_type == 0:
        return jsonify(random_key())
    elif encrypt_type == 1:
        return jsonify(random_key(24))
    elif encrypt_type == 2:
        return jsonify(random_key(32))


@app.route("/aes_encryption", methods=["GET"])
def aes_encryption():
    """"""
    try:
        string = request.headers.get("AES-String")
        cipher_key = request.headers.get("Cipher-Key")
        encrypt_type = request.headers.get("Encryption-Type")
    except:
        return jsonify(False), 500
    # encrypt_type is 0 for 128 bit, 1 for 192 bit, 2 for 256 bit
    if string[:2] != "0x":
        string = str2hex(string)
    encrypted = aes_encrypt(str2hex(cipher_key), string, int(encrypt_type)).encrypt()
    return jsonify({"string": hex2str(encrypted), "hex": encrypted})


@app.route("/aes_decryption", methods=["GET"])
def aes_decryption():
    try:
        string = request.headers.get("AES-String")
        cipher_key = request.headers.get("Cipher-Key")
        encrypt_type = request.headers.get("Encryption-Type")
    except:
        return jsonify(False), 500
    # encrypt_type is 0 for 128 bit, 1 for 192 bit, 2 for 256 bit
    if string[:2] != "0x":
        string = str2hex(string)
    decrypted = aes_decrypt(str2hex(cipher_key), string, int(encrypt_type)).decrypt()
    return jsonify({"string": hex2str(decrypted), "hex": decrypted})


app.run(host="127.7.3.0", port=1728, debug=True)
