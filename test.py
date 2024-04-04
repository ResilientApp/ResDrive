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

# set_value("test", "\n")
# set_value("test public_key", "\n")
a = {"a": {"b": {}}}
print(len(a['a']['b']))

