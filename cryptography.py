import os
import time
import json
from Crypto.Cipher import AES
from fastecdsa.curve import P256
from fastecdsa.point import Point
from fastecdsa import keys, curve, ecdsa
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_keys(S, st):
    delta = round(time.time()) - st
    R = S * delta
    priv_key = R.x
    pub_key = keys.get_public_key(priv_key, curve.P256)
    return (delta, priv_key , pub_key)

def sign_message(message, S, st):
    delta, priv_key, pub_key = get_keys(S, st)
    r, s = ecdsa.sign(message, priv_key)
    return(r, s, pub_key)

def encrypt(message, pswd, iv):
    obj = AES.new(pswd, AES.MODE_CFB, iv)
    ciphertxt =  obj.encrypt(message)
    return ciphertxt

def decrypt (ciphertxt, pswd, iv):
    obj = AES.new(pswd, AES.MODE_CFB, iv)
    mssg = obj.decrypt(ciphertxt)
    return mssg

def create_encrypted_json(data, sx, sy, st, pswd, iv):
    data_str = str(data)
    encrypted_data = encrypt(data_str, pswd, iv)
    S = Point(int(sx, 0), int(sy, 0), curve=P256)
    r, s, pk = sign_message(data_str, S, st)
    encrypted_r = encrypt(str(r), pswd, iv)
    encrypted_s = encrypt(str(s), pswd, iv)
    encrypted_pk = encrypt(str(pk), pswd, iv)
    encrypted_st = encrypt(str(st), pswd, iv)
    output = {"data": encrypted_data, "r": encrypted_r, "s": encrypted_s, "pn": encrypted_st,"pk": encrypted_pk}
    return output

def decrypt_json_data(encrypted_data, pswd, iv):
    decrypted_data = {}
    for k in encrypted_data.keys():
        decrypted_data[k] = decrypt(encrypted_data[k], pswd, iv).decode('UTF-8')
    return decrypted_data

def check_signature(r, s, pk_string, data):
    n_r = int(r)
    n_s = int(s)
    pk = pk_string.split('\n')
    x = pk[0].split()[1]
    y = pk[1].split()[1]
    S = Point(int(x, 0), int(y, 0), curve=P256)
    valid = ecdsa.verify((n_r, n_s), data, S)
    return valid


if __name__ == "__main__":

    # Get parameters from parameter file
    path = os.path.join(os.path.dirname(__file__),'parameters.json' )
    with open(path) as f:
        parameters = json.load(f)

    key =  parameters["KEY"]
    iv = parameters["IV"]
    sx = parameters["SX"]
    sy = parameters["SY"]
    st = parameters["ST"]

    # Create Fake Data
    data = {"id": "12344", "name": "sample_name", "agency": "sample_agency", "date_time": "sample_date_time"}
    print(data)

    # Encrypted Data
    encrypted_data = create_encrypted_json(data, sx, sy, st, key, iv)
    print(encrypted_data)

    # Decrypted Data
    decrypted_data = decrypt_json_data(encrypted_data, key, iv)
    print(decrypted_data)

    # Check if signature is Valid
    check_signature(decrypted_data['r'], decrypted_data['s'], decrypted_data['pk'], decrypted_data['data'])
