# ResDrive
A decentralized personal cloud based on ResilientDB blockchain and IPFS cluster

## How to run
### System requirement
1. A running IPFS entry point(Please follow [Link](https://docs.ipfs.tech/install/ipfs-desktop/) to deploy IPFS Desktop on Ubuntu or [Link](https://docs.ipfs.tech/install/run-ipfs-inside-docker/) deploy IPFS through Docker)
2. Ubuntu 22.04 LTS
3. Python 3.10
4. bazel 5.0 or 7.0 `sudo apt install bazel-5.0.0`
5. Python packages:
   1. pycryptodome `pip isntall pycryptodome`
   2. pybind11 `pip install pybind11`
   3. cryptography `pip install cryptography`
   4. ipfshttpclient `pip install ipfshttpclient==0.8.0a2`(Please ignore the warning message of the daemon version)

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