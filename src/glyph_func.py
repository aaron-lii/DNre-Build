"""
计算glyph属性
"""
import json

from src.tool_func import add_dicts, get_my_path


# 加载数据
with open(get_my_path('data/glyph.json'), 'r', encoding='utf-8') as file:
    glyph_json = json.load(file)


def get_glyph_state(glyph_names_list,
                    glyph_p_names_list):
    """ 统计纹章属性 """
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


def glyph_func(input_list):
    """ 主入口 """
    glyph_names = input_list[: 11]
    glyph_p_names = input_list[11: 22]

    glyph_state = get_glyph_state(glyph_names, glyph_p_names)
    # print(glyph_state)

    return glyph_state


