# ResDrive
A decentralized personal cloud based on ResilientDB blockchain and IPFS cluster

## Key features
1. Decentralized Architecture: Our system avoids the need for a central server. All messages are transmitted through 
ResilientDB blockchain and IPFS cluster.
2. Data storage: Metadata are stored in ResilientDB blockchain i.e. file structure, file hash etc. Files are stored in
IPFS cluster.
3. Security: All the data stored in ResilientDB and in IPFS are encrypted by Fernet


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
   5. psutil `pip install psutil`

### Start Service
1. cd to `kv-service_python_api` directory
2. Run `bazel build :pybind_kv_so` to build ResilientDB kv-service Python API
3. Start client `python start_client.py`

## Operations
1. `cd`: Change to target directory`cd [target directory name]`
2. `ls`: Will list all contents under this directory
3. `mkdir`: Create a new directory under your current directory `mkdir [new directory name]`
4. `rm`: Delete a directory `rm [target directory name]`
5. `upload`: Upload single/multiple file(s) `upload [file/directory path]`(If the path is a directory, system will scan and 
upload every file, even those files in nested directories)
6. `download`: Download single/multiple file(s) `download [file/directory name] [(optional)Path to save file(s)]`
(If the second parameter is not specified, file(s) will download into downloads directory under ResDrive directory)
7. `back`: Go back to previous directory, no parameter needed
8. `share`: UNDER DEVELOPING
9. `detail`: Show file detail `detail [file name]`
10. `root`: GO back to `/root` directory, no parameter needed