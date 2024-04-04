import json

import util
import sys
import os

sys.path.append('kv-service_python_api/')
from kv_operation import get_value, set_value

username = None
public_key = None
private_key = None
file_structure = {}
current_location = ["root"]
fernet_key = None
util.clear_screen()
if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem") or not os.path.exists("fernet.key"):
    print("No RSA keypair found, please create user")
    while True:
        username_in = input("Please input your username: ")
        password_in = input("Please input your password: ")
        result = util.create_user(username_in, password_in)
        if not result:
            util.clear_screen()
            print("Username has already taken, please try another one")
        else:
            util.clear_screen()
            print("Sign up successfully, please login")
            break


while True:
    username_in = input("Username: ")
    password_in = input("Password: ")
    public_key, private_key = util.load_rsa_keypair(username_in, password_in)
    if public_key is None and private_key is None:
        util.clear_screen()
        print("Wrong username or password, please try again")
    else:
        print("Login successfully")
        username = username_in
        fernet_key = util.load_fernet_key()
        print("loading information")
        break

file_structure = json.loads(util.decrypt_message_with_rsa(private_key, get_value(username)))
util.clear_screen()
print("Welcome to ResDrive!")
print("Type help to see commands")

while True:
    operation = input("/" + "/".join(current_location) + " >").split()

    # 处理ls指令
    if operation[0] == "ls":
        inner_folder = util.get_inner_folder(file_structure, current_location)
        for names in inner_folder.keys():
            print(names, end="\t" + "\t")
        print("\n")

    # 处理cd指令
    elif operation[0] == "cd":
        if len(operation) != 2:
            print("Please follow: cd [target folder]")
        else:
            target_folder_name = operation[1]
            # 尝试获取新的目标目录
            new_location = current_location + [target_folder_name]
            inner_folder = util.get_inner_folder(file_structure, new_location)
            if inner_folder is not None:
                # 如果目标目录存在，更新current_location
                current_location = new_location
            else:
                print(f"{target_folder_name}: No such folder")

    # 处理rm指令
    elif operation[0] == "rm":
        inner_folder = util.get_inner_folder(file_structure, current_location)
        # TODO:没完事

    elif operation[0] == "mkdir":
        if len(operation) != 2:
            print("Please follow: mkdir [new folder name]")
        else:
            new_folder_name = operation[1]
            file_structure = util.create_folder(file_structure, current_location, new_folder_name)
            encrypted_fs = util.encrypt_message_with_rsa(public_key, json.dumps(file_structure))
            set_value(username, encrypted_fs)
            print(f"Folder '{new_folder_name}' created.")
    elif operation[0] == "quit" or operation[0] == "q":
        break
    elif operation[0] == "upload":
        pass
    elif operation[0] == "download":
        pass
    elif operation[0] == "root":
        current_location = ['root']
    elif operation[0] == "back":
        current_location.pop()
    elif operation[0] == "clear":
        util.clear_screen()
    elif operation[0] == "share":
        pass
    else:
        pass


