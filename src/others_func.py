"""
计算others属性
"""

import json
from src.tool_func import job_info_dict, add_dicts


# 加载数据
with open('data/appellation.json', 'r', encoding='utf-8') as file:
    appellation_json = json.load(file)
with open('data/collection.json', 'r', encoding='utf-8') as file:
    collection_json = json.load(file)
with open('data/skill.json', 'r', encoding='utf-8') as file:
    skill_json = json.load(file)


def get_appellation_state(appellation_name):
    """ 统计appellation属性 """
    state_dict = {}
    if appellation_name not in ["无", ""]:
        state_dict = appellation_json[appellation_name]
    return state_dict


def get_collection_state(collection_num):
    """ 统计collection属性 """
    state_dict_list = []
    collection_json_list = []
    for i in range(1, 7):
        collection_json_list.append(collection_json[str(i)])
    for i in range(collection_num):
        state_dict_list.append(collection_json_list[i % 6])

    return add_dicts(state_dict_list)


def get_skill_state(job, skill_levels):
    """ 统计skill属性 """
    base_skill_name_list = list(skill_json["被动"]["通用"].keys())
    job_skill_name_list = []
    if job in skill_json["被动"]:
        job_skill_name_list = list(skill_json["被动"][job].keys())
    personal_skill_name_list = []
    if job in skill_json["个人buff"]:
        personal_skill_name_list = list(skill_json["个人buff"][job].keys())
    team_skill_name_list = list(skill_json["团队buff"].keys())

    state_dict_list = []
    for i in range(len(base_skill_name_list)):
        state_now = {}
        for state_name, state_val_list in skill_json["被动"]["通用"][base_skill_name_list[i]].items():
            if skill_levels[: 3][i] > 0:
                state_now[state_name] = state_val_list[skill_levels[: 3][i] - 1]
        state_dict_list.append(state_now)

    for i in range(len(job_skill_name_list)):
        state_now = {}
        for state_name, state_val_list in skill_json["被动"][job][job_skill_name_list[i]].items():
            if skill_levels[3: 6][i] > 0:
                state_now[state_name] = state_val_list[skill_levels[3: 6][i] - 1]
        state_dict_list.append(state_now)

    for i in range(len(personal_skill_name_list)):
        state_now = {}
        for state_name, state_val_list in skill_json["个人buff"][job][personal_skill_name_list[i]].items():
            if skill_levels[6: 9][i] > 1:
                state_now[state_name] = state_val_list[skill_levels[6: 9][i] - 1]
        state_dict_list.append(state_now)

    for i in range(len(team_skill_name_list)):
        state_now = {}
        for state_name, state_val_list in skill_json["团队buff"][team_skill_name_list[i]].items():
            if skill_levels[9: 15][i] > 1:
                state_now[state_name] = state_val_list[skill_levels[9: 15][i] - 1]
        state_dict_list.append(state_now)

    return add_dicts(state_dict_list)


def others_func(job, input_list):
    # 计算称号属性
    appellation_name = input_list[0]
    appellation_state = get_appellation_state(appellation_name)
    # print(appellation_state)

    # 计算时装收藏属性
    collection_num = input_list[1]
    collection_state = get_collection_state(collection_num)
    # print(collection_state)

    # 计算技能增加的属性
    skill_levels = input_list[2: 17]
    skill_state = get_skill_state(job, skill_levels)
    # print(skill_state)

    return add_dicts([appellation_state, collection_state]), skill_state



