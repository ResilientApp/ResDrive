import os.path
import json
import util
import base64
import binascii
import datetime
import json
import os
import platform
import sys
import ipfshttpclient
import psutil

sys.path.append('kv-service_python_api/')
from kv_operation import get_value, set_value

username = None
public_key = None
private_key = None
file_structure = {}
current_location = ["root"]
fernet_key = None
ipfs_config = None


def login(username_in: str, password_in: str) -> int:
    """
    登录
    返回0：登陆成功
    返回1：钥匙不存在
    返回2：密码错误
    返回3：IPFS接入点配置文件不存在
    返回4：用户不存在
    """
    global public_key, private_key, username, ipfs_config, file_structure
    if os.path.exists("private_key.pem") and os.path.exists("fernet.key") and os.path.exists("public_key.pem"):
        if not os.path.exists("ipfs.config"):
            return 3
        else:
            if get_value(username_in) == "\n" or get_value(username_in) == "" or get_value(username_in) == " ":
                return 4
            public_key, private_key = util.load_rsa_keypair(username_in, password_in)
            ipfs_config = util.load_config()
            file_structure = json.loads(fernet_key.decrypt((get_value(username)).encode()))
            if public_key is None or private_key is None:
                return 2
            else:
                username = username_in
                return 0
    else:
        return 1


def sign_up(username_in, password_in):
    """
    创建用户
    返回0：成功
    返回1：用户名或密码错误
    返回2：用户名已经被使用
    """
    if os.path.exists("private_key.pem") and os.path.exists("fernet.key") and os.path.exists("public_key.pem"):
        return 1
    else:
        result = util.create_user(username_in, password_in)
        if not result:
            return 2
        else:
            login(username_in, password_in)
            return 0
