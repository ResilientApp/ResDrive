import json
import threading

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
ipfs_config = None


def update_structure_with_file_info(file_name, file_hash: list, file_size_mb, upload_time):
    global file_structure, current_location
    # 初始化dict_pointer指向file_structure的根
    dict_pointer = file_structure["/root"]

    # 遍历current_location来定位到正确的目录
    # 注意，这里我们跳过了列表的第一个元素"root"，因为我们已经开始于"/root"
    for folder in current_location[1:]:
        if "/" + folder not in dict_pointer:
            # 如果路径不存在，则创建新目录
            dict_pointer["/" + folder] = {}
        dict_pointer = dict_pointer["/" + folder]

    # 在当前位置添加或更新文件信息
    dict_pointer[file_name] = {
        "hash": file_hash,
        "size_mb": file_size_mb,
        "upload_time": upload_time.isoformat()  # 使用ISO格式的字符串表示时间
    }


def encapsulated_download(download_target: str, save_path='downloads'):
    download_inner_folder = util.get_inner_folder(file_structure, current_location)
    if (not download_target.startswith('/')) and download_target in download_inner_folder:
        file_detail = download_inner_folder[download_target]
        util.download_single_file(file_detail['hash'], download_target, fernet_key, ipfs_config, save_path)
        return
    elif download_target.startswith('/') and download_target in download_inner_folder:
        folder_detail = download_inner_folder[download_target]
        for file_name, file_info in folder_detail.items():
            util.download_single_file(file_info['hash'], file_name, fernet_key, ipfs_config, save_path)
        return
    else:
        print(f"{download_target} does not exist.")
        return


def encapsulated_upload(path):
    if os.path.isfile(path):
        file_name, file_hash_list, file_size_mb, upload_time = util.upload_single_file(path, fernet_key, ipfs_config)
        update_structure_with_file_info(file_name, file_hash_list, file_size_mb, upload_time)
    elif os.path.isdir(path):
        file_path_list, res_list = [], []

        for root, dirs, files in os.walk(path):
            for name in files:
                file_path = str(os.path.join(root, name))
                file_path_list.append(file_path)

        user_in = input(
            f"There are total {len(file_path_list)} files found, do you want to upload them all? [y]/no: ")
        user_in = user_in.lower()
        if user_in == 'y' or user_in == 'yes':
            for file_path in file_path_list:
                file_name, file_hash_list, file_size_mb, upload_time = util.upload_single_file(file_path,
                                                                                               fernet_key,
                                                                                               ipfs_config)
                res_list.append([file_name, file_hash_list, file_size_mb, upload_time])

            for res in res_list:
                update_structure_with_file_info(res[0], res[1], res[2], res[3])
        else:
            print("Upload stopped.")
            return
    else:
        print(f"{path} does not exist.")
        return

    set_value(username, fernet_key.encrypt((json.dumps(file_structure)).encode()))
    return


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
        print("loading information")
        username = username_in
        fernet_key = util.load_fernet_key()
        ipfs_config = util.load_config()
        break

file_structure = json.loads(fernet_key.decrypt(get_value(username)))
util.clear_screen()
print("Welcome to ResDrive!")
print("Type help to see commands")

while True:
    operation = input("/" + "/".join(current_location) + " >").split()
    # print("------------"+json.dumps(file_structure, indent=4))  # 查看更新后的结构
    if len(operation) == 0:
        print("Operation unidentified.\nPlease use help command to show operations")
        continue
    # 处理ls指令
    if operation[0] == "ls":
        file_structure = json.loads(fernet_key.decrypt((get_value(username)).encode()))
        inner_folder = util.get_inner_folder(file_structure, current_location)
        # print("+++++++++++" + json.dumps(inner_folder))
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
        if len(operation) != 2:
            print("Please follow: rm [target name]")
        else:
            target_name = operation[1]
            # 获取当前位置的文件结构
            inner_folder = util.get_inner_folder(file_structure, current_location)
            if target_name in inner_folder:
                target_path = target_name
            else:
                # 定位到要删除的目标
                target_path = "/" + target_name  # 确保路径格式一致
            if target_path in inner_folder:
                if len(inner_folder) != 0 and target_path.startswith('/'):
                    answer = input(
                        f"{target_name} is not empty, rm will remove all contents inside this folder, "
                        f"do you want to continue [y]/n: ")
                    answer = answer.lower()
                    if answer == "y" or answer == "yes":
                        # 执行删除操作
                        del inner_folder[target_path]
                        print(f"{target_name} has been removed.")
                        # 加密并保存更新后的文件结构
                        encrypted_fs = fernet_key.encrypt((json.dumps(file_structure)).encode())
                        set_value(username, encrypted_fs)
                else:
                    # 执行删除操作
                    del inner_folder[target_path]
                    print(f"{target_name} has been removed.")
                    # 加密并保存更新后的文件结构
                    encrypted_fs = fernet_key.encrypt((json.dumps(file_structure)).encode())
                    set_value(username, encrypted_fs)
            else:
                print(f"{target_name}: No such file or folder")
    elif operation[0] == "mkdir":
        if len(operation) != 2:
            print("Please follow: mkdir [new folder name]")
        else:
            new_folder_name = operation[1]
            file_structure = util.create_folder(file_structure, current_location, new_folder_name)
            encrypted_fs = fernet_key.encrypt((json.dumps(file_structure)).encode())
            set_value(username, encrypted_fs)

    elif operation[0] == "quit" or operation[0] == "q":
        break
    elif operation[0] == "upload":
        if len(operation) != 2:
            print("Please follow: upload [file/folder location]")
        else:
            # print(operation[1])
            upload_thread = threading.Thread(target=encapsulated_upload, args=(operation[1],))
            upload_thread.start()
            continue
            # upload_thread.join()
    elif operation[0] == "download":
        if len(operation) != 2 and len(operation) != 3:
            print("Please follow: download [file/folder name] [path to save]")
        else:
            if len(operation) == 2:
                download_thread = threading.Thread(target=encapsulated_download, args=(operation[1],))
                download_thread.start()
                continue
                # download_thread.join()
            else:
                download_thread = threading.Thread(target=encapsulated_download, args=(operation[1], operation[2],))
                download_thread.start()
                continue
                # download_thread.join()
    elif operation[0] == "root":
        current_location = ['root']
    elif operation[0] == "back":
        if current_location == ['root']:
            print("You already at /root")
        else:
            current_location.pop()
    elif operation[0] == "clear":
        util.clear_screen()
    elif operation[0] == "share":
        pass
    elif operation[0] == 'detail':
        if len(operation) != 2:
            print("Please follow: detail [filename]")
        else:
            file_name = operation[1]
            inner_folder = util.get_inner_folder(file_structure, current_location)
            if file_name in inner_folder:
                file_detail = inner_folder[file_name]
                upload_date = file_detail['upload_time']
                size_mb = file_detail['size_mb']
                print(f"File name: {file_name} \t\t File size: {size_mb}MB \t\t Upload Date: {upload_date}")
    elif operation[0] == 'help':
        os.system('cat ops.txt')
        print()
    else:
        pass
