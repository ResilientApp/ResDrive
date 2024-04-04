import sys
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
parent_dir = os.path.dirname(current_dir)

sys.path.append(os.path.join(parent_dir, "kv-service_python_api", "bazel-out", "k8-fastbuild", "bin"))
print(os.path.join(parent_dir, "kv-service_python_api", "bazel-out", "k8-fastbuild", "bin"))
import pybind_kv

config_path = current_dir + "/kv_server.config"


def set_value(key: str, value: str):
    pybind_kv.set(str("resdrive" + key), value, config_path)


def get_value(key: str) -> str:
    return pybind_kv.get(str("resdrive" + key), config_path)
