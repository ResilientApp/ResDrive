import datetime
import json
import os.path

import psutil
import sys
import math
import util

sys.path.append("kv-service_python_api")
from kv_operation import get_value, set_value
# client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
# res = client.add('test.jpeg')
# file_hash = res['Hash']
# print(file_hash)
#
# set_value("test", "\n")
# set_value("test public_key", "\n")
# pub, pri = util.load_rsa_keypair("test", "test")
fernet_key = util.load_fernet_key()
set_value("test", fernet_key.encrypt((json.dumps({'/root': {}})).encode()))






