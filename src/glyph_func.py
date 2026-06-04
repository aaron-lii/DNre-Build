"""
计算glyph属性
"""
from src.tool_func import add_dicts, glyph_json, glyph2_json, glyph_plus_by_glyph_json


def _expedition_level_numeric(level_key: str) -> int:
    digits = ''.join(ch for ch in str(level_key) if ch.isdigit())
    return int(digits) if digits else 0


def _is_multi_level_expedition_data():
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return False
    first_key = next(iter(glyph2_json.keys()))
    first_val = glyph2_json[first_key]
    return isinstance(first_val, dict) and "base" not in first_val and "plus" not in first_val


def _get_expedition_level_keys():
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return []
    if _is_multi_level_expedition_data():
        return sorted(glyph2_json.keys(), key=_expedition_level_numeric)
    return ["默认"]


def _get_default_expedition_level_key():
    keys = _get_expedition_level_keys()
    return keys[-1] if keys else "默认"


def _get_expedition_names():
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return []
    if _is_multi_level_expedition_data():
        keys = _get_expedition_level_keys()
        if not keys:
            return []
        return list(glyph2_json[keys[0]].keys())
    return list(glyph2_json.keys())


def _get_expedition_level_data(level_key: str):
    if not isinstance(glyph2_json, dict) or not glyph2_json:
        return {}
    if _is_multi_level_expedition_data():
        if level_key not in glyph2_json:
            level_key = _get_default_expedition_level_key()
        return glyph2_json.get(level_key, {})
    return glyph2_json


def _get_expedition_base_labels(glyph_name: str, level_key: str):
    expedition_data = _get_expedition_level_data(level_key)
    base_dict = expedition_data.get(glyph_name, {}).get("base", {})
    if glyph_name == "攻击之远征队纹章":
        return ["物攻", "魔攻"]
    return list(base_dict.keys())


def get_glyph_state(glyph_names_list,
                    glyph_p_names_list):
    """ 统计普通纹章属性 (原有11条) """
    state_dict_list = []
    for i in range(len(glyph_names_list)):
        lv_name_now = glyph_names_list[i]
        if lv_name_now in ["无", ""]:
            continue
        lv_now, name_now = lv_name_now.split("-", 1)
        # 基础属性
        state_dict_list.append(glyph_json["base"][lv_now][name_now])
        # 三属性
        name_p_now = glyph_p_names_list[i]
        if name_p_now not in ["无", ""]:
            state_dict_list.append(_get_glyph_plus_state(lv_now, name_now, name_p_now))

    return add_dicts(state_dict_list)


def _get_glyph_plus_state(level_key: str, glyph_name: str, plus_name: str):
    plus_by_glyph = glyph_plus_by_glyph_json or glyph_json.get("plus_by_glyph", {})
    glyph_plus_dict = plus_by_glyph.get(level_key, {}).get(glyph_name)
    if glyph_plus_dict is not None:
        return glyph_plus_dict.get(plus_name, {})
    return glyph_json["plus"][level_key].get(plus_name, {})


def _parse_expedition(expedition_input_list):
    """解析远征队纹章追加的组件列表 (顺序: 每种 = 等级 + base... + plus)。"""
    if not expedition_input_list:
        return {}
    state_dict_list = []
    expedition_names = _get_expedition_names()
    level_keys = _get_expedition_level_keys()
    default_level_key = _get_default_expedition_level_key()
    cursor = 0
    for glyph_name in expedition_names:
        level_key = expedition_input_list[cursor] if cursor < len(expedition_input_list) else default_level_key
        cursor += 1
        if level_key not in level_keys:
            level_key = default_level_key
        attr_name_list = _get_expedition_base_labels(glyph_name, level_key)
        for attr_name in attr_name_list:
            val_str = expedition_input_list[cursor] if cursor < len(expedition_input_list) else "无"
            cursor += 1
            if val_str in ["无", "", None]:
                continue
            try:
                val_int = int(val_str)
            except Exception:
                continue
            if glyph_name == "攻击之远征队纹章" and attr_name == "物攻":
                for k in ["最小物攻", "最大物攻"]:
                    state_dict_list.append({k: val_int})
            elif glyph_name == "攻击之远征队纹章" and attr_name == "魔攻":
                for k in ["最小魔攻", "最大魔攻"]:
                    state_dict_list.append({k: val_int})
            else:
                state_dict_list.append({attr_name: val_int})
        plus_str = expedition_input_list[cursor] if cursor < len(expedition_input_list) else "无"
        cursor += 1
        if plus_str not in ["无", "", None]:
            try:
                attr_plus, val_plus = plus_str.rsplit("+", 1)
                val_plus_int = int(val_plus)
                if glyph_name == "攻击之远征队纹章" and attr_plus == "物攻":
                    for k in ["最小物攻", "最大物攻"]:
                        state_dict_list.append({k: val_plus_int})
                elif glyph_name == "攻击之远征队纹章" and attr_plus == "魔攻":
                    for k in ["最小魔攻", "最大魔攻"]:
                        state_dict_list.append({k: val_plus_int})
                else:
                    state_dict_list.append({attr_plus: val_plus_int})
            except Exception:
                pass
    return add_dicts(state_dict_list)


def glyph_func(input_list, player_level: str = "60"):
    """ 主入口 (兼容附加远征队纹章) """
    # 原有结构: 0-10 base 组合, 11-21 plus 三属性
    # 追加: 远征队每种 = 等级 + base 数值选择 + plus
    glyph_names = input_list[: 11]
    glyph_p_names = input_list[11: 22]
    expedition_part = input_list[22:]

    glyph_state = get_glyph_state(glyph_names, glyph_p_names)
    expedition_state = _parse_expedition(expedition_part)

    return add_dicts([glyph_state, expedition_state])
