"""
计算致命、最终、防御的百分比
"""


def calculate_critical_percent(input_num):
    """ 致命百分比 """
    critical_rate = 167.6
    critical_percent = min(round(input_num / critical_rate, 1), 90)

    return critical_percent


def calculate_final_atk_percent(input_num):
    """ 计算最终伤害的百分比 """
    final_atk_rate1 = 34
    # 75-79之间都有可能
    final_atk_rate2 = 75

    # 为了方便观察距离下一个百分点还多远，保留一位小数
    final_atk_percent = round(input_num / final_atk_rate1, 1)

    if final_atk_percent > 45:
        final_atk_percent = 45 + round((input_num - 45 * final_atk_rate1) / final_atk_rate2, 1)

    return final_atk_percent


def calculate_def_percent(input_num):
    """ 根据数值计算防御百分比 """

    # 防御计算规则参数（分阶段递增）
    stages = [
        {"max_percent": 55, "cost_per_pct": 99.86},  # 阶段1：0-55%
        {"max_percent": 63, "cost_per_pct": 243.7},  # 阶段2：56-63%
        {"max_percent": 66, "cost_per_pct": 415},  # 阶段3：64-66%
        {"max_percent": 69, "cost_per_pct": 465},  # 阶段4：67-69%
        {"max_percent": 100, "cost_per_pct": 562}  # 阶段5：70-100%
    ]

    remaining = float(input_num)
    total_percent = 0.0

    for i, stage in enumerate(stages):

        if i == 0:
            max_cost = stage["max_percent"] * stage["cost_per_pct"]
        else:
            max_cost = (stage["max_percent"] - stages[i - 1]["max_percent"]) * stage["cost_per_pct"]

        if remaining >= max_cost:
            total_percent = stage["max_percent"]
            remaining -= max_cost
        else:
            add_pct = remaining / stage["cost_per_pct"]
            total_percent += add_pct
            break  # 数值不足以进入下一阶段

    # 限制最大100%，保留1位小数
    return round(min(total_percent, 100.0), 1)
