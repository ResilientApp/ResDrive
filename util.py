import base64
import binascii
import json
import os
import platform
import sys

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet

sys.path.append("kv-service_python_api")
from kv_operation import get_value, set_value


def load_config():
    # 读取.config文件
    with open('server_config.config', 'r') as f:
        ipfs = f.readline().split(' ')
        ipfs_ip = ipfs[0]
        ipfs_port = int(ipfs[1])
        return ipfs_ip, ipfs_port


def load_rsa_keypair(username: str, password: str):
    if os.path.exists('private_key.pem') and os.path.exists('public_key.pem'):
        with open('public_key.pem', 'rb') as f:
            public_key = RSA.import_key(f.read())
        try:
            with open("private_key.pem", "rb") as f:
                private_key = RSA.import_key(f.read(), passphrase=username + password)
        except Exception as e:
            print("Error loading private key:", str(e))
            return None, None
        return public_key, private_key


def load_fernet_key():
    if os.path.exists('fernet.key'):
        with open('fernet.key', 'rb') as f:
            fernet_key = f.read()
        return Fernet(fernet_key)


def public_key_to_string(public_key_bytes):
    return base64.b64encode(public_key_bytes).decode('utf-8')


def string_to_public_key(pub_key_string):
    return RSA.importKey(pub_key_string.encode('utf-8'))


def encrypt_message_with_rsa(pub_key, message: str or bytes):
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    if type(message) is str:
        message = message.encode()
    encrypted_message = cipher_rsa.encrypt(message)
    encrypted_message = binascii.hexlify(encrypted_message).decode('ascii')
    return encrypted_message


def decrypt_message_with_rsa(pri_key, enc_message):
    # 将十六进制字符串转换为字节
    encrypted_message_bytes = binascii.unhexlify(enc_message)

    # 创建PKCS1_OAEP对象用于解密
    cipher_rsa = PKCS1_OAEP.new(pri_key)

    # 解密消息
    decrypted_message = cipher_rsa.decrypt(encrypted_message_bytes)

    # 将字节解码成字符串
    return decrypted_message.decode('utf-8')


def get_inner_folder(file_structure: dict, current_folder: list) -> dict:
    sub_folder = file_structure
    for i in current_folder:
        sub_folder_name = "/" + i
        sub_folder = sub_folder.get(sub_folder_name)
    return sub_folder


def create_user(username: str, password: str) -> bool:
    user_info = get_value(username)
    if user_info == "" or user_info == "\n":
        rsa_key = RSA.generate(2048)
        fernet_key = Fernet.generate_key()
        with open("fernet.key", "wb") as key_file:
            key_file.write(fernet_key)
        private_key = rsa_key.exportKey(passphrase=username + password, pkcs=8)
        public_key_str = rsa_key.publickey().export_key()
        public_key = rsa_key.public_key()
        with open(f"private_key.pem", "wb") as f:
            f.write(private_key)
        with open(f"public_key.pem", "wb") as f:
            f.write(public_key_str)
        set_value(username, encrypt_message_with_rsa(public_key, json.dumps({"/root": {}})))
        set_value(username + " public_key", public_key_str)
        return True
    else:
        return False


def clear_screen():
    """
    Clears the terminal screen.
    """
    # 检查操作系统
    os_name = platform.system()
    if os_name == "Windows":
        # 如果是Windows系统，使用cls命令
        os.system('cls')
    else:
        # 对于Linux和Mac，使用clear命令
        os.system('clear')


def encrypt_file_with_fernet(fernet_key, file):
    encrypted_data = fernet_key.encrypt(file)
    return encrypted_data


def decrypt_file_with_fernet(fernet_key, encrypted_file):
    decrypted_data = fernet_key.decrypt(encrypted_file)
    return decrypted_data


def create_folder(file_structure, current_location, new_folder_name):
    # Navigate to the current location in the file structure
    current_dict = file_structure
    for folder in current_location:  # 假设current_location不包含前导'/'
        folder_path = "/" + folder  # 如果file_structure的键以'/'开头
        current_dict = current_dict.setdefault(folder_path, {})

    # 当前current_dict指向current_location指定的最深层字典
    # Create the new folder in the current location
    new_folder_path = "/" + new_folder_name  # 保持一致的路径命名规则
    if new_folder_path not in current_dict:
        current_dict[new_folder_path] = {}
    else:
        print(f"Folder '{new_folder_name}' already exists at {'/'.join(current_location)}")

    return file_structure
