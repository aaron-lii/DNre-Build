"""
计算surplus属性
"""

from src.tool_func import add_dicts, surplus_json


def get_surplus_state(surplus_levels):
    surplus_name_list = ["伤害增加", "受伤减少", "最大生命值", "最大魔法值",
                         "物理攻击力", "魔法攻击力", "物理防御", "魔法防御",
                         "致命一击", "最终伤害", "致命一击抵抗", "魔法值恢复",
                         "硬直", "硬直抵抗", "眩晕", "眩晕抵抗"]

    state_dict_list = []
    for i in range(len(surplus_levels)):
        if surplus_levels[i] == 0:
            continue
        surplus_name_now = surplus_name_list[i]
        surplus_level_now = surplus_levels[i]
        if surplus_json[surplus_name_now] == {}:
            continue
        state_name_list = list(surplus_json[surplus_name_now].keys())
        for state_name_now in state_name_list:
            state_dict_list.append({state_name_now:
                                    surplus_json[surplus_name_now][state_name_now][surplus_level_now - 1]})

    return add_dicts(state_dict_list)


def surplus_func(input_list):
    """ 主入口 """
    surplus_levels = input_list[: 16]
    surplus_state = get_surplus_state(surplus_levels)
    # print(surplus_state)

    return surplus_state
