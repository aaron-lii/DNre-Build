"""
计算rune属性
"""
import json

from src.tool_func import add_dicts, get_my_path


# 加载数据
with open(get_my_path('data/rune.json'), 'r', encoding='utf-8') as file:
    rune_json = json.load(file)


def get_rune_state(rune_names,
                   rune_ps):
    state_dict_list = []
    for i in range(len(rune_names)):
        if rune_names[i] in ["无", ""]:
            continue
        state_now = {rune_names[i]: int(rune_ps[i])}
        state_dict_list.append(state_now)

    return add_dicts(state_dict_list)


def rune_func(input_list):
    """ 主入口 """
    rune_names = input_list[: 16]
    rune_ps = input_list[16: 32]

    rune_state = get_rune_state(rune_names, rune_ps)
    # print(rune_state)

    return rune_state
