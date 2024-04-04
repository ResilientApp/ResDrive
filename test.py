import json

import ipfshttpclient, sys
from cryptography.fernet import Fernet

import util
sys.path.append("kv-service_python_api")
from kv_operation import get_value, set_value
# client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
# res = client.add('test.jpeg')
# file_hash = res['Hash']
# print(file_hash)

# set_value("aaa", "\n")
# print(get_value("test public_key"))
# util.string_to_public_key(get_value("test public_key"))
#
# fernet_key = Fernet.generate_key()
# print(type(fernet_key.decode()))

# pub, pri = util.load_rsa_keypair("test", "test")
#
# enc = util.encrypt_message_with_rsa(pub, "test")
# dec = util.decrypt_message_with_rsa(pri, enc)
#
# print(dec)

pub, pri = util.load_rsa_keypair("test", "test")
set_value("test", util.encrypt_message_with_rsa(pub, json.dumps({"/root": {}})))

