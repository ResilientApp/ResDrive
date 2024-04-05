import base64
import binascii
import datetime
import json
import os
import platform
import sys
import ipfshttpclient
import psutil

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet

sys.path.append("kv-service_python_api")
from kv_operation import get_value, set_value


def load_config():
    # 读取.config文件
    with open('ipfs.config', 'r') as f:
        return f.readline()


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
        print(f"Folder '{new_folder_name}' created.")
    else:
        print(f"Folder '{new_folder_name}' already exists at {'/'.join(current_location)}")

    return file_structure


def upload_single_file(file_path: str, fernet_key, ipfs_config):
    client = ipfshttpclient.connect(ipfs_config)
    chunk_size = int(psutil.virtual_memory().available * 0.01)

    # 确保临时目录存在
    tmp_upload_dir = "tmp_upload"
    os.makedirs(tmp_upload_dir, exist_ok=True)

    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        file_size_mb = round(os.path.getsize(file_path) / 1024 / 1024, 2)
        hash_list = []
        count = 0
        with open(file_path, 'rb') as input_file:
            while True:
                chunk = input_file.read(chunk_size)
                if not chunk:
                    time_uploaded = datetime.datetime.now()
                    break  # 文件读取完成

                encrypted_chunk = fernet_key.encrypt(chunk)
                encrypted_file_path = os.path.join(tmp_upload_dir, f"{file_name}_{count}.encrypt")
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_chunk)

                res = client.add(encrypted_file_path)
                hash_list.append(res['Hash'])

                # 删除临时加密文件块
                os.remove(encrypted_file_path)

                count += 1

        print(f"{file_name} uploaded successfully")
    else:
        print(f"{file_path} does not exist")
        return None

    return file_name, hash_list, file_size_mb, time_uploaded

# def upload_single_file(file_path: str, fernet_key, ipfs_config):
#     client = ipfshttpclient.connect(ipfs_config)
#     chunk_size = int(psutil.virtual_memory().available * 0.01)
#
#     # 确保临时目录存在
#     os.makedirs("tmp_upload", exist_ok=True)
#
#     if os.path.exists(file_path):
#         file_name = os.path.basename(file_path)
#         # 使用完整路径获取文件大小
#         file_size_mb = round(os.path.getsize(file_path) / 1024 / 1024, 2)
#
#         encrypted_file_path = os.path.join("tmp_upload", file_name + ".encrypt")
#         with open(file_path, 'rb') as input_file, open(encrypted_file_path, 'wb') as encrypted_file:
#             while True:
#                 chunk = input_file.read(chunk_size)
#                 if not chunk:
#                     break  # 文件读取完成
#
#                 encrypted_chunk = fernet_key.encrypt(chunk)
#                 encrypted_file.write(encrypted_chunk)
#
#         res = client.add(encrypted_file_path)
#         time_uploaded = datetime.datetime.now()
#         file_hash = res['Hash']
#         print(f"{file_name} uploaded successfully")
#         # 删除临时加密文件
#         os.remove(encrypted_file_path)
#     else:
#         print(f"{file_path} does not exist")
#         return None
#     return file_name, file_hash, file_size_mb, time_uploaded
#
#


def download_single_file(file_hash: list, file_name: str, fernet_key, ipfs_config, save_path='downloads'):
    client = ipfshttpclient.connect(ipfs_config)
    # 确保下载目录存在
    os.makedirs('tmp_download', exist_ok=True)
    os.makedirs('downloads', exist_ok=True)

    # 完整的保存路径
    final_path = os.path.join(save_path, file_name)

    with open(final_path, 'wb') as final_file:
        for h in file_hash:
            # 临时下载路径
            # temp_download_path = os.path.join('tmp_download', h)

            # 从IPFS下载加密的文件块
            client.get(h, target='tmp_download')

            # 读取、解密、写入
            with open('tmp_download/' + h, 'rb') as temp_file:
                encrypted_chunk = temp_file.read()
                decrypted_chunk = fernet_key.decrypt(encrypted_chunk)
                final_file.write(decrypted_chunk)

            # 删除临时下载的加密文件块
            os.remove(f'tmp_download/{h}')

    print(f"{file_name} downloaded and decrypted successfully")
    return



# def download_single_file(file_hash, file_name, fernet_key, ipfs_config, save_path):
#     client = ipfshttpclient.connect(ipfs_config)
#     chunk_size = int(psutil.virtual_memory().available * 0.01)
#     # 确保下载目录存在
#     os.makedirs(save_path, exist_ok=True)
#
#     # 临时下载路径
#     temp_download_path = os.path.join("tmp_download", file_hash)
#
#         # 从IPFS下载加密的文件
#         client.get(file_hash, target="tmp_download")
#
#         # 完整的保存路径
#         temp_download_path = os.path.join("tmp_download", file_hash)
#
#         # 打开加密的文件，解密，然后保存解密后的内容
#         with open(temp_download_path, 'rb') as encrypted_file, open(final_path, 'wb') as decrypted_file:
#             while True:
#                 # 读取加密文件的一部分
#                 encrypted_chunk = encrypted_file.read(chunk_size)
#                 if not encrypted_chunk:
#                     break  # 文件读取完成
#
#                 # 解密并写入到最终文件
#                 decrypted_chunk = fernet_key.decrypt(encrypted_chunk)
#                 decrypted_file.write(decrypted_chunk)
#
#         print(f"{file_name} downloaded and decrypted successfully")

#
#     finally:
#         # 清理：删除临时下载的加密文件
#         if os.path.exists(temp_download_path):
#             os.remove(temp_download_path)
