# ResDrive
A decentralized personal cloud based on ResilientDB blockchain and IPFS cluster

## Key features
1. Decentralized Architecture: Our system avoids the need for a central server. All messages are transmitted through 
ResilientDB blockchain and IPFS cluster.
2. Data storage: Metadata are stored in ResilientDB blockchain i.e. file structure, file hash etc. Files are stored in
IPFS cluster.
3. Security: All the data stored in ResilientDB blockchain are encrypted by RSA. Files are broken into chunks and
encrypted by Fernet stored in IPFS cluster


## How to run
### System requirement
1. A running IPFS entry point(Please follow [Link](https://docs.ipfs.tech/install/ipfs-desktop/) to deploy IPFS 
Desktop on Ubuntu or [Link](https://docs.ipfs.tech/install/run-ipfs-inside-docker/) deploy IPFS through Docker)
2. Ubuntu 22.04 LTS
3. Python 3.10
4. bazel 5.0 or 7.0 `sudo apt install bazel-5.0.0`
5. Python packages:
   1. pycryptodome `pip isntall pycryptodome`
   2. pybind11 `pip install pybind11`
   3. cryptography `pip install cryptography`
   4. ipfshttpclient `pip install ipfshttpclient==0.8.0a2`(Please ignore the warning message of the daemon version)
   5. psutil

### Start Service
1. cd to `kv-service_python_api` folder
2. Run `bazel build :pybind_kv_so`
3. Start client `python start_client.py`

## Operations
1. `cd`: Change to target folder`cd [TARGET_FOLDER]`
2. `ls`: Will list all contents under this folder
3. `mkdir`: Create a new folder under your current directory `mkdir [NEW_FOLDER_NAME]`
4. `rm`: Delete a folder `rm [TARGET_FOLDER_NAME]`
5. `upload`:
6. `download`:
7. `back`: Go back to previous folder
8. `share`:
9. `detail`: