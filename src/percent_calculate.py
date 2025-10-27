"""
计算致命、最终、防御的百分比
"""
from src.tool_func import player_common_level_json


def calculate_critical_percent(input_num, player_level=50):
    """ 致命百分比 """
    critical_90 = player_common_level_json[str(player_level)]["_Ccritical"] * 0.9
    critical_rate = critical_90 / 90

    critical_percent = min(round(input_num / critical_rate, 1), 90)

    return critical_percent


def calculate_final_atk_percent(input_num, player_level=50):
    """ 计算最终伤害的百分比 """
    base_damage = player_common_level_json[str(player_level)]["_Cfinaldamage"]
    # 计算阈值点（对应45%的伤害值）
    threshold = 0.45 * base_damage / 0.8

    final_atk_rate1 = threshold / 45
    final_atk_rate2 = (base_damage - threshold) / 15

    # 为了方便观察距离下一个百分点还多远，保留一位小数
    final_atk_percent = round(input_num / final_atk_rate1, 1)

    if final_atk_percent > 45:
        final_atk_percent = 45 + round((input_num - threshold) / final_atk_rate2, 1)

    return final_atk_percent


def calculate_defense_percent(input_num, player_level=50):
    """ 计算防御百分比 """
    fixed_value = 20

    # 获取当前等级的未知值
    level_reduction_coefficients_base = player_common_level_json[str(player_level - 1)]["_CdefenseNew1"]

    if level_reduction_coefficients_base < 0:
        # 低等级（未知值为负）：使用动态公式
        reduction = max(50, 741 - 0.975 * input_num)
    else:
        # 高等级（未知值为正）：使用"等级+5"规则
        lookup_level = min(player_level + 5, 100)
        unknown = player_common_level_json[str(lookup_level - 1)]["_CdefenseNew1"]
        reduction = unknown + fixed_value

    # 计算防御率
    defense_rate = input_num / (input_num + reduction)

    # 防御率上限
    max_rate = 0.999899983406067
    defense_rate = min(defense_rate, max_rate)

    return round(defense_rate * 100, 1)
