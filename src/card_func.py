"""
计算card属性
"""
import json

from src.tool_func import add_dicts, get_my_path


# 加载数据
with open(get_my_path('data/card_skill.json'), 'r', encoding='utf-8') as file:
    card_skill_json = json.load(file)
with open(get_my_path('data/card.json'), 'r', encoding='utf-8') as file:
    card_json = json.load(file)


def get_card_state(card_skills,
                   cards):
    card_skill_list = list(card_skill_json.keys())
    card_name_list = list(card_json.keys())

    state_dict_list = []
    for i in range(len(cards)):
        if cards[i] in ["无", ""]:
            continue
        state_now = card_json[card_name_list[i]][cards[i]]
        state_dict_list.append(state_now)
    all_state = add_dicts(state_dict_list)

    res_state = {}
    for i in range(len(card_skills)):
        state_name = card_skill_json[card_skill_list[i]]["属性"]
        if card_skills[i] == 0:
            state_num = 0
        else:
            state_num = card_skill_json[card_skill_list[i]]["数值"][card_skills[i] - 1]

        if state_name in all_state:
            res_state[state_name] = int(all_state[state_name] * (1 + state_num))

    return res_state


def card_func(input_list):
    """ 主入口 """
    card_skills = input_list[: 12]
    cards = input_list[12: len(input_list)]

    card_state = get_card_state(card_skills, cards)
    # print(rune_state)

    return card_state
