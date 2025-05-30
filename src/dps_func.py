"""
计算dps
"""

import json

from src.percent_calculate import calculate_critical_percent
from src.tool_func import get_my_path

# 加载数据
with open(get_my_path('data/boss.json'), 'r', encoding='utf-8') as file:
    boss_json = json.load(file)

atk_type_dict = {"光": ["光攻%", "光抗%"],
                 "暗": ["暗攻%", "暗抗%"],
                 "火": ["火攻%", "火抗%"],
                 "水": ["水攻%", "水抗%"]}


def single_dps_func(input_list):
    """
    计算单属性dps
    输出期望=(面板x技能百分比+技能固伤)x(1+属性攻)x(1-属性抗)x(1+暴击率x(1-暴击抵抗率))x(1+最终伤害)x(1+其他增伤)
    """
    atk_type1, atk_type2, atk_num1, atk_num2, target_boss, final_state, glyph_plus = input_list

    if atk_type1 == "物攻":
        atk_num = (final_state["最小物攻"] + final_state["最大物攻"]) / 2
    else:
        atk_num = (final_state["最小魔攻"] + final_state["最大魔攻"]) / 2

    # 这里先不做归一化
    dps_part1 = atk_num * atk_num1 / 100 + atk_num2

    # 计算属性乘区
    if atk_type2 == "无":
        dps_part2 = 1
    else:
        dps_part2 = (1 + final_state[atk_type_dict[atk_type2][0]]) \
                    * (1 - boss_json[target_boss][atk_type_dict[atk_type2][1]])

    # 计算暴击率乘区
    dps_part3 = 1 + final_state["致命百分比"] / 100 * \
                (1 - calculate_critical_percent(boss_json[target_boss]["致命抵抗"]) / 100)

    # 计算最终乘区
    dps_part4 = 1 + final_state["最终百分比"] / 100 + glyph_plus / 100

    # 计算其他乘区
    dps_part5 = 1 + final_state["额外伤害%"]

    return dps_part1 * dps_part2 * dps_part3 * dps_part4 * dps_part5


def dps_func(input_list):
    """
    计算混合dps
    """
    (atk_type1, atk_type2, atk_num1, atk_num2, glyph_plus1,
     atk_type3, atk_type4, atk_num3, atk_num4, glyph_plus3,
     atk_type5, atk_type6, atk_num5, atk_num6, glyph_plus5,
     target_boss, final_state) = input_list

    atk_num_all = 0
    dps_all = 0
    for (atk_type1_now, atk_type2_now, atk_num1_now,
         atk_num2_now, glyph_plus1) in [(atk_type1, atk_type2, atk_num1, atk_num2, glyph_plus1),
                                        (atk_type3, atk_type4, atk_num3, atk_num4, glyph_plus3),
                                        (atk_type5, atk_type6, atk_num5, atk_num6, glyph_plus5)]:
        if atk_type1_now != "无" and atk_num1_now > 0:
            atk_num_all += atk_num1_now / 100
            dps_all += single_dps_func([atk_type1_now, atk_type2_now,
                                        atk_num1_now, atk_num2_now,
                                        target_boss, final_state, glyph_plus1])
    # 归一化到技能面板为100%
    return round(dps_all / atk_num_all, 2)


def def_func(input_list):
    """
    用一击秒杀伤害衡量生存期望
    一击秒杀x(1-防御百分比)x(1+boss暴击率x(1-暴击抵抗率))=血量
    生存期望=血量/(1-防御百分比)/(1+boss暴击率x(1-暴击抵抗率))
    """
    atk_type1, atk_type2, atk_num1, atk_num2, glyph_plus, \
    _, _, _, _, _, _, _, _, _, _, \
    target_boss, final_state, def_type = input_list

    # 计算防御乘区
    if def_type == "物防":
        def_part1 = 1 - final_state["防御百分比"] / 100
    else:
        def_part1 = 1 - final_state["魔防百分比"] / 100

    # 计算暴击抵抗乘区
    def_part2 = 1 + calculate_critical_percent(boss_json[target_boss]["致命"]) / 100 * \
                (1 - calculate_critical_percent(final_state["致命抵抗"]) / 100)

    return round(final_state["HP"] / def_part1 / def_part2, 2)
