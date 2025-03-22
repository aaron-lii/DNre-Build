"""
计算skin属性
"""

import json

from src.tool_func import add_dicts, get_my_path


# 加载数据
with open(get_my_path('data/skin.json'), 'r', encoding='utf-8') as file:
    skin_json = json.load(file)


def get_skin_state(skin_names):
    state_dict_list = []
    type_list = ["weapon1_skin", "weapon2_skin",
                 "wing_skin", "tail_skin", "printing_skin",
                 "necklace_skin", "earrings_skin", "ring_skin", "ring_skin"]
    for i in range(len(skin_names)):
        if skin_names[i] in ["无", ""]:
            continue
        type_now = type_list[i]
        state_dict_list.append(skin_json[type_now][skin_names[i]])

    return add_dicts(state_dict_list)


def skin_func(input_list):
    """ 主入口 """
    skin_names = input_list[: 9]
    skin_state = get_skin_state(skin_names)
    # print(skin_state)

    return skin_state

