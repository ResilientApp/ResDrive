# ResDrive
A decentralized personal cloud based on ResilientDB blockchain and IPFS cluster

## How to run
### System requirement
1. Ubuntu 22.04 LTS
2. Python 3.10
3. bazel 5.0 or 7.0 `sudo apt install bazel-5.0.0`
4. Python packages:
   1. pycryptodome `pip isntall pycryptodome`
   2. pybind11 `pip install pybind11`
   3. cryptography `pip install cryptography`

### Start Service
1. cd to `kv-service_python_api` folder
2. Run `bazel build :pybind_kv_so`
3. Start client `python start_client.py`

## Operations
1. `cd`:
2. `ls`:
3. `mkdir`:
4. `rm`:
5. `login`:
6. `signup`:
7. `upload`:
8. `download`:
9. `cd..`: