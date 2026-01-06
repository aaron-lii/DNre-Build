"""
一些通用函数
"""
import sys
import os
import logging
import requests
import json

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger()
# 避免重复添加多个handler
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


# 中阶职业 -> 基础职业（职业大类）
job_info_dict = {"剑圣": "战士", "战神": "战士", "箭神": "弓箭", "游侠": "弓箭",
                 "元素": "法师", "魔导": "法师", "祭司": "牧师", "贤者": "牧师",
                 "工程": "学者", "炼金": "学者", "呐喊者": "舞娘", "舞者": "舞娘",
                 "复仇者": "战士"}

# 高阶职业 -> 中阶职业（转职后关联）
job_info_dict2 = {"剑皇": "剑圣", "月之领主": "剑圣", "狂战士": "战神", "毁灭者": "战神",
                  "狙翎": "箭神", "魔羽": "箭神", "影舞者": "游侠", "风行者": "游侠",
                  "火舞": "元素", "冰灵": "元素", "时空领主": "魔导", "黑暗女王": "魔导",
                  "圣骑士": "贤者", "十字军": "贤者", "圣徒": "祭司", "雷神": "祭司",
                  "重炮手": "工程", "机械大师": "工程", "炼金圣士": "炼金", "药剂师": "炼金",
                  "黑暗萨满": "呐喊者", "噬魂者": "呐喊者", "刀锋舞者": "舞者", "灵魂舞者": "舞者",
                  "黑暗复仇者": "复仇者"}

# 装备表内使用的职业代码映射（NeedJobClass）
JOB_CLASS_CODE_MAP_EQUIPMENT = {
    1: "战士", 2: "弓箭", 3: "法师", 4: "牧师", 5: "学者", 6: "舞娘",
    11: "剑圣", 12: "战神", 14: "箭神", 15: "游侠",
    17: "元素", 18: "魔导", 20: "贤者", 22: "祭司",
    46: "工程", 49: "炼金", 54: "呐喊者", 57: "舞者",
    75: "复仇者"
}

# 高阶职业代码（角色等级表等使用）
JOB_CLASS_CODE_MAP_ADVANCED = {
    23: "剑皇", 24: "月之领主", 25: "狂战士", 26: "毁灭者",
    29: "狙翎", 30: "魔羽", 31: "影舞者", 32: "风行者",
    35: "火舞", 36: "冰灵", 37: "时空领主", 38: "黑暗女王",
    41: "圣骑士", 42: "十字军", 43: "圣徒", 44: "雷神",
    47: "重炮手", 48: "机械大师", 50: "炼金圣士", 51: "药剂师",
    55: "黑暗萨满", 56: "噬魂者", 58: "刀锋舞者", 59: "灵魂舞者",
    76: "黑暗复仇者"
}

# 高阶职业顺序列表（用于下拉显示）
ADVANCED_JOBS_ORDERED = [
    "剑皇", "月之领主", "狂战士", "毁灭者",
    "狙翎", "魔羽", "影舞者", "风行者",
    "火舞", "冰灵", "时空领主", "黑暗女王",
    "圣骑士", "十字军", "圣徒", "雷神",
    "重炮手", "机械大师", "炼金圣士", "药剂师",
    "黑暗萨满", "噬魂者", "刀锋舞者", "灵魂舞者",
    "黑暗复仇者"
]

# 主页面职业下拉使用（包含提示项）
JOBS_DROPDOWN_LIST = ["请选择你的职业"] + ADVANCED_JOBS_ORDERED


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
        with open(get_my_path("update_logs.txt"), "r", encoding='utf-8') as f_r:
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


# 统一数据加载与缓存
_DATA_CACHE: dict[str, dict] = {}


def _load_json_file(file_name: str):
    """ 读取并缓存 data 目录下的 JSON 文件 """
    if file_name not in _DATA_CACHE:
        path = get_my_path(f"data/{file_name}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                _DATA_CACHE[file_name] = json.load(f)
        except FileNotFoundError:
            logger.error(f"数据文件缺失: {file_name}")
            _DATA_CACHE[file_name] = {}
        except Exception as e:  # noqa: F841
            logger.exception(f"加载数据文件出错: {file_name}")
            _DATA_CACHE[file_name] = {}
    return _DATA_CACHE[file_name]


def load_json(short_name: str):
    """ 按约定名称获取 JSON 数据

    short_name 例如: 'equipment_base' 对应 data/equipment_base.json
    """
    return _load_json_file(f"{short_name}.json")

# 提前加载（首次 import 时）
appellation_json = load_json('appellation')
collection_json = load_json('collection')
skill_json = load_json('skill')
glyph_json = load_json('glyph')
rune_json = load_json('rune')
surplus_json = load_json('surplus')
skin_json = load_json('skin')
equipment_base_json = load_json('equipment_base')
equipment_suffix_json = load_json('equipment_suffix')
equipment_group_json = load_json('equipment_group')
equipment_grade_json = load_json('equipment_grade')
equipment_enchant_json = load_json('equipment_enchant')
jewelry_json = load_json('jewelry')
player_base_state_json = load_json('player_base')
player_common_level_json = load_json('player_common_level')
state_rate_json = load_json('state_rate')
boss_json = load_json('boss')
dps_type_json = load_json('dps_type')
card_skill_json = load_json('card_skill')
card_json = load_json('card')
glyph2_json = load_json('glyph2')

# 额外的派生结构：附魔名称 -> 属性 dict
enchant_json = {}
if equipment_enchant_json:
    for _type, val in equipment_enchant_json.items():
        for name, state_dict in val.items():
            enchant_json[name] = state_dict


# 这里直接获取版本号
version, data_version = get_version()
# 这里直接获取当前环境
env_now = get_env()
# 获取最新版本号
remote_version_info = get_remote_version(version)
