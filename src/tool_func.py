"""
一些通用函数
"""
import sys
import os
import logging
import requests

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


job_info_dict = {"剑圣": "战士", "战神": "战士", "箭神": "弓箭", "游侠": "弓箭",
                 "元素": "法师", "魔导": "法师", "祭司": "牧师", "贤者": "牧师",
                 "工程": "学者", "炼金": "学者"}

job_info_dict2 = {"剑皇": "剑圣", "月之领主": "剑圣", "狂战士": "战神", "毁灭者": "战神",
                  "狙翎": "箭神", "魔羽": "箭神", "影舞者": "游侠", "风行者": "游侠",
                  "火舞": "元素", "冰灵": "元素", "时空领主": "魔导", "黑暗女王": "魔导",
                  "圣骑士": "贤者", "十字军": "贤者", "圣徒": "祭司", "雷神": "祭司",
                  "重炮手": "工程", "机械大师": "工程", "炼金圣士": "炼金", "药剂师": "炼金"}


def get_env():
    """ 判断当前运行环境 """
    if getattr(sys, 'frozen', False):
        # 如果是打包后的程序
        return "exe"
    else:
        return "py"


def get_my_path(input_path):
    """ 根据运行环境修改相对路径 """
    env_now = get_env()
    if env_now == "exe":
        # 如果是打包后的程序
        base_path = sys._MEIPASS
    else:
        # 如果是开发环境
        base_path = os.path.abspath(".")

    out_path = os.path.join(base_path, input_path)

    return out_path


def add_dicts(dict_lists: list[dict]):
    """ 合并属性字典 """
    res_dict = {}
    for dict_now in dict_lists:
        for key, val in dict_now.items():
            if key in res_dict:
                if "%" in str(key):
                    res_dict[key] += val
                else:
                    # 客户端中每步计算都取了int
                    res_dict[key] += int(val)
            else:
                if "%" in str(key):
                    res_dict[key] = val
                else:
                    res_dict[key] = int(val)

    return res_dict


def get_version():
    """ 获取本地版本号 """
    version_now = ""
    data_version_now = ""
    try:
        with open(get_my_path("update_logs.txt"), "r") as f_r:
            line_all = f_r.readlines()
            version_now = line_all[0].strip().split(": ", 1)[1]
            data_version_now = line_all[1].strip().split(": ", 1)[1]
    except Exception as e:
        logger.warning("本地版本号获取失败")

    return version_now, data_version_now


def get_remote_version(local_version):
    """ 获取最新版本号 """
    url = "https://www.modelscope.cn/studio/aaronL/DNre-Build/resolve/master/update_logs.txt"

    try:
        response = requests.get(url, timeout=5)
        res_text = response.text
        remote_version = res_text.split("\n", 1)[0].split(": ", 1)[1]
        if remote_version == local_version:
            res_info = local_version + "  已是最新版"
        else:
            res_info = remote_version + \
                       '  <span style="color:red; font-weight:bold;">有更新！</span>'
    except Exception as e:
        logger.warning("最新版本号获取失败")
        res_info = "最新版本号获取失败"

    return res_info


# 这里直接获取版本号
version, data_version = get_version()
# 这里直接获取当前环境
env_now = get_env()
# 获取最新版本号
remote_version_info = get_remote_version(version)
