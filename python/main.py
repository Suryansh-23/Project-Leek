import json
from AES import aes_encrypt, aes_decrypt
from Steganography import stegano_encrypt, stegano_decrypt
from Encoder import Vault

from random import choices
from string import ascii_letters, digits
from json import loads
from zipfile import ZipFile
from os import rename, path

from flask import Flask
from flask import jsonify, request


AUTH = ""  # AUTH (global var) for maintaining a valid Auth-Key to be used to verify connection with authenticated clients only


def random_key(k: int = 16):
    """Generates a random auth key"""
    # encrypt_type is 0 for 128 bit, 1 for 192 bit, 2 for 256 bit
    str_pool = ascii_letters + digits
    return "".join(choices(str_pool, k=k))


def str2hex(s: str):
    main = "0x"
    for i in s:
        tmp = hex(ord(i)).lstrip("0x")
        if len(tmp) < 2:
            tmp = "0" + tmp
        main += tmp
    return main


def hex2str(hex: str):
    hex = hex[2:]
    chrs = [hex[i : i + 2] for i in range(0, len(hex), 2)]
    s = ""
    for i in chrs:
        n = int(f"0x{i}", 16)
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
        string = json.loads(request.headers.get("AES-String"))
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


@app.route("/file_vault", methods=["GET"])
def file_vault():
    try:
        pswrd = request.headers.get("Password")
        vault_path = request.headers.get("Vault-Path")
        file_paths = loads(request.headers.get("File-Paths"))

        with ZipFile(
            ".\\python\\File-Vault-v1.0.0-win32-x64.zip",
            "r",
        ) as z:
            z.extractall(vault_path)
            rename(
                vault_path + r"\\File-Vault-v1.0.0-win32-x64",
                vault_path + r"\\Vault",
            )

        main = Vault(
            Pswrd=pswrd, path=vault_path + "\\Vault", file_paths=file_paths, tui=False
        )
        main.main()
        return jsonify(True)
    except:
        return jsonify(False), 500


@app.route("/stegano_encryption", methods=["GET"])
def stegano_encryption():
    try:
        img = loads(request.headers.get("Img-Addr"))
        data = request.headers.get("String")

        for i in img:
            name = path.split(path.splitext(i)[0])[1]
            folder = path.split(i)[0]
            fp = folder + "\\" + name + "_Encrypted" + ".png"
            stegano_obj = stegano_encrypt(data=data, img=i, fp=fp)
            stegano_obj.encrypt()

        return jsonify(True)
    except:
        return jsonify(False), 500


@app.route("/stegano_decryption", methods=["GET"])
def stegano_decryption():
    try:
        img = loads(request.headers.get("Img-Addr"))

        main = {}
        for i in img:
            stegano_obj = stegano_decrypt(img=i)
            main[path.basename(i)] = stegano_obj.decrypt()

        return jsonify(main)
    except:
        return jsonify(False), 500


app.run(host="127.7.3.0", port=2302)
