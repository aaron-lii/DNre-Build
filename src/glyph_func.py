"""
计算glyph属性
"""
from src.tool_func import add_dicts, glyph_json, glyph2_json


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
            state_dict_list.append(glyph_json["plus"][lv_now][name_p_now])

    return add_dicts(state_dict_list)


def _parse_expedition(expedition_input_list):
    """ 解析远征队纹章追加的组件列表 (顺序: 所有 base 数值选择 + 每种一个 plus) """
    if not expedition_input_list:
        return {}
    state_dict_list = []
    expedition_names = list(glyph2_json.keys())
    # 计算每个 glyph 的 base 属性数量 (考虑攻击之远征队纹章合并为2条)
    expedition_base_attr_names = []
    for g_name in expedition_names:
        base_dict = glyph2_json[g_name]["base"]
        if g_name == "攻击之远征队纹章":
            expedition_base_attr_names.append(["物攻", "魔攻"])  # 合并后UI提供
        else:
            expedition_base_attr_names.append(list(base_dict.keys()))
    base_counts = [len(x) for x in expedition_base_attr_names]
    total_base = sum(base_counts)
    base_values = expedition_input_list[: total_base]
    plus_values = expedition_input_list[total_base: ]

    cursor = 0
    for i, glyph_name in enumerate(expedition_names):
        base_attr_dict = glyph2_json[glyph_name]["base"]
        attr_name_list = expedition_base_attr_names[i]
        for attr_name in attr_name_list:
            val_str = base_values[cursor] if cursor < len(base_values) else "无"
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
        plus_str = plus_values[i] if i < len(plus_values) else "无"
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


def glyph_func(input_list):
    """ 主入口 (兼容附加远征队纹章) """
    # 原有结构: 0-10 base 组合, 11-21 plus 三属性
    # 追加: 远征队 base 数值选择 (合并后11个) + 远征队 plus (4个) 共15个
    glyph_names = input_list[: 11]
    glyph_p_names = input_list[11: 22]
    expedition_part = input_list[22:]

    glyph_state = get_glyph_state(glyph_names, glyph_p_names)
    expedition_state = _parse_expedition(expedition_part)

    return add_dicts([glyph_state, expedition_state])
