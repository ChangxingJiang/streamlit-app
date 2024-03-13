"""
工具方法
"""

import os
import sys

from streamlit_app.errors import StreamlitAppDeployError


def clear_folder(folder_path: str) -> None:
    """清空文件夹

    Parameters
    ----------
    folder_path : str
        文件夹的路径
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            clear_folder(file_path)
            os.rmdir(file_path)


def remove_py_suffix(file_name: str) -> str:
    """剔除 py 脚本的 .py 或 .pyc 后缀"""
    if file_name.endswith(".py"):
        return file_name[:-3]
    if file_name.endswith(".pyc"):
        return file_name[:-4]
    return file_name


def get_import_name_by_file_path(file_path: str) -> str:
    """根据文件路径获取 Python 的 import 引用路径

    检索规则：
    1. 寻找最长的引用路径，即使用最接近根目录的 sys.path，从而避免相同路径引用失败的情况。
    2. 如果当前文件 / 文件名名称不是字母、数字或下划线组成，则说明该路径不能是 Python 引用路径，结束匹配

    Parameters
    ----------
    file_path : str
        Python 脚本文件路径

    Raises
    ------
    StreamlitAppDeployError
        无法获取到目标 Python 脚本的引用路径（即当前 Python 脚本当前无法引用进来）
    """
    # 处理入口脚本：module 为 __main__，引用时 module 使用当前文件名即可
    if file_path == sys.argv[0]:
        module_path = remove_py_suffix(os.path.basename(file_path))
        print(f"Python 脚本: {file_path}, 入口脚本, 引用路径: {module_path}")
        return module_path

    # 处理非入口脚本
    for module_path, module_obj in sys.modules.copy().items():
        if module_obj.__class__.__name__ != "module":
            continue  # 跳过不为 module 的情况

        module_spec = module_obj.__spec__
        if module_spec is None:
            continue  # 跳过 __main__ 或 cython 相关

        module_origin = module_spec.origin
        if module_origin in {"built-in", "frozen"}:
            continue  # 跳过内置模块

        if module_origin == file_path:
            print(f"Python 脚本: {file_path}, 非入口脚本, 引用路径: {module_path}")
            return module_path
    else:
        raise StreamlitAppDeployError(f"找不到 Python 脚本的 module: 脚本路径={file_path}")
