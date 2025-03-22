"""
计算equipment属性
"""
import json
import copy

from src.tool_func import job_info_dict, job_info_dict2, add_dicts, get_my_path


# 加载数据
with open(get_my_path('data/equipment_base.json'), 'r', encoding='utf-8') as file:
    equipment_base_json = json.load(file)
with open(get_my_path('data/equipment_suffix.json'), 'r', encoding='utf-8') as file:
    equipment_suffix_json = json.load(file)
with open(get_my_path('data/equipment_group.json'), 'r', encoding='utf-8') as file:
    equipment_group_json = json.load(file)
with open(get_my_path('data/equipment_grade.json'), 'r', encoding='utf-8') as file:
    equipment_grade_json = json.load(file)
with open(get_my_path('data/equipment_enchant.json'), 'r', encoding='utf-8') as file:
    equipment_enchant_json = json.load(file)
    enchant_json = {}
    for key, val in equipment_enchant_json.items():
        for key2, val2 in val.items():
            enchant_json[key2] = val2
    del equipment_enchant_json
with open(get_my_path('data/jewelry.json'), 'r', encoding='utf-8') as file:
    jewelry_json = json.load(file)


def get_equip_state(job,
                    equip_names_list,
                    suffix_names_list,
                    grade_nums_list):
    """ 统计武器防具相关属性 """
    group_dict = {}
    state_dict_list = []
    for i in range(len(equip_names_list)):
        # 基础属性的处理逻辑
        item_now = equip_names_list[i]
        if item_now in ["无", ""]:
            continue
        # print(item_now)
        lv, equip_name_now = item_now.split("-", 1)

        # 升星基础属性不变
        star_num = 0
        if "★" in equip_name_now:
            star_num = equip_name_now.count("★")
            equip_name_now = equip_name_now.replace("★", "")

        # 非L装在基础职业里面
        if "L" in lv:
            # 转为一转职业
            job_now = job_info_dict2[job]
        else:
            # 转为基础职业
            job_now = job_info_dict[job_info_dict2[job]]

        state_base = equipment_base_json[job_now][lv][equip_name_now]["属性"]
        group_id_now = equipment_base_json[job_now][lv][equip_name_now]["套装"]
        if group_id_now not in group_dict:
            group_dict[group_id_now] = 1
        else:
            group_dict[group_id_now] += 1
        state_dict_list.append(state_base)

        # 后缀的处理逻辑
        suffix_now = suffix_names_list[i]
        state_suffix = equipment_suffix_json[job_now][lv][equip_name_now][suffix_now]
        state_dict_list.append(state_suffix)

        # 强化的处理逻辑
        grade_now = grade_nums_list[i]
        if grade_now == 0:
            continue
        state_grade = copy.deepcopy(equipment_grade_json[job_now][lv][equip_name_now][str(grade_now)])
        star_rate = 1 + star_num * 0.08
        for key, val in state_grade.items():
            state_grade[key] = val * star_rate
        state_dict_list.append(state_grade)

    # 返回装备属性 和套装情况
    return add_dicts(state_dict_list), group_dict


def get_jewelry_state(jewelry_names_list,
                      jewelry_state_list):
    """ 统计首饰相关属性 """
    group_dict = {}
    state_dict_list = []
    for i in range(len(jewelry_names_list)):
        if jewelry_names_list[i] in ["无", ""]:
            continue
        lv_now, jewelry_name_now = jewelry_names_list[i].split("-", 1)
        state_i_now = jewelry_state_list[i].split(":", 1)[0]
        is_get_state = False
        for part, val1 in jewelry_json.items():
            for lv, val2 in val1.items():
                if lv != lv_now:
                    continue
                if jewelry_name_now in val2:
                    state_now = val2[jewelry_name_now]["属性"][state_i_now]
                    group_id_now = val2[jewelry_name_now]["套装"]
                    state_dict_list.append(state_now)
                    if group_id_now not in group_dict:
                        if group_id_now != 0:
                            group_dict[group_id_now] = 1
                    else:
                        group_dict[group_id_now] += 1
                    break
            if is_get_state:
                break

    # 返回首饰属性 和套装情况
    return add_dicts(state_dict_list), group_dict


def get_enchant_state(equip_names,
                      enchant_lists):
    """ 统计附魔相关属性 """
    state_dict_list = []
    for i in range(len(equip_names)):
        if equip_names[i] in ["无", ""]:
            continue
        for enchant_now in enchant_lists[i]:
            state_dict_list.append(enchant_json[enchant_now])

    return add_dicts(state_dict_list)


def get_group_state(group_dict):
    """ 统计套装属性 """
    state_dict_list = []
    for group_id, group_num in group_dict.items():
        group_id = str(group_id)
        if group_num > 1:
            for i in range(2, group_num + 1):
                if str(i) in equipment_group_json[group_id]["属性"]:
                    state_dict_list.append(equipment_group_json[group_id]["属性"][str(i)])

    return add_dicts(state_dict_list)


def equipment_func(job, input_list):
    """ 主入口 """
    equip_names = input_list[: 7]
    suffix_names = input_list[7: 14]
    grade_nums = input_list[14: 21]
    equip_enchant_lists = input_list[21: 28]
    jewelry_names = input_list[28: 32]
    jewelry_state_i = input_list[32: 36]
    jewelry_enchant_lists = input_list[36: 40]

    # 装备属性
    equip_states, equip_group = get_equip_state(job,
                                                equip_names,
                                                suffix_names,
                                                grade_nums)
    # print(equip_states, equip_group)

    # 首饰属性
    jewelry_states, jewelry_group = get_jewelry_state(jewelry_names,
                                                      jewelry_state_i)
    # print(jewelry_states, jewelry_group)

    # 装备附魔
    equip_enchant_states = get_enchant_state(equip_names,
                                             equip_enchant_lists)
    # print(equip_enchant_states)

    # 首饰附魔
    jewelry_enchant_states = get_enchant_state(jewelry_names,
                                               jewelry_enchant_lists)
    # print(jewelry_enchant_states)

    # 套装属性
    group_states = get_group_state(add_dicts([equip_group, jewelry_group]))
    # print(group_states)

    all_states = add_dicts([equip_states, jewelry_states,
                            equip_enchant_states, jewelry_enchant_states,
                            group_states])

    return all_states



