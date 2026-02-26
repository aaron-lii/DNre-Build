"""
计算rune属性
"""
from src.tool_func import add_dicts


def _parse_enhance_level(val):
    """解析源铸石板强化等级(0-10)。"""
    if val in [None, "", "无"]:
        return 0
    try:
        level = int(float(str(val).strip()))
    except Exception:
        return 0
    return max(0, min(level, 10))


def _apply_enhance_bonus(rune_state: dict, enhance_level: int):
    """按强化等级对石板总属性做百分比加成。"""
    if enhance_level <= 0 or not rune_state:
        return rune_state
    ratio = 1 + enhance_level / 100
    return {k: int(v * ratio) for k, v in rune_state.items()}


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
    rune_names = input_list[: 24]
    rune_ps = input_list[24: 48]
    core_rune_enhance = input_list[51] if len(input_list) > 51 else 0

    rune_state = get_rune_state(rune_names, rune_ps)
    enhance_level = _parse_enhance_level(core_rune_enhance)
    rune_state = _apply_enhance_bonus(rune_state, enhance_level)
    # print(rune_state)

    return rune_state
