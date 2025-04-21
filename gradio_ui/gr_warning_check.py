"""
用于检测数据合法性
"""

import gradio as gr


def check_glyph(glyph_list):
    """ 检查纹章 """
    glyph_now_list = []
    for glyph_now in glyph_list[:11]:
        if glyph_now == "无":
            continue
        glyph_now = glyph_now.split("-", 1)[1]
        if glyph_now in glyph_now_list:
            gr.Warning("不能选择重复的纹章: " + glyph_now)
            break
        else:
            glyph_now_list.append(glyph_now)


def check_equipment(equipment_list):
    """ 检查装备后缀 """
    equip_list = equipment_list[: 7]
    suffix_list = equipment_list[7: 14]

    for i in range(len(equip_list)):
        if "40A" in equip_list[i] and "II" in suffix_list[i]:
            gr.Warning(equip_list[i] + " 没有后缀: " + suffix_list[i])
        elif "40S" in equip_list[i] and "II" in suffix_list[i]:
            gr.Warning(equip_list[i] + " 没有后缀: " + suffix_list[i])


def check_rune(rune_list):
    """ 检查石板 """
    rune_names = rune_list[: 24]

    for i in range(4):
        rune_name_dict = {}
        for j in range(6):
            rune_name_now = rune_names[i * 6 + j]
            if rune_name_now == "无":
                continue
            if rune_name_now not in rune_name_dict:
                rune_name_dict[rune_name_now] = 1
            else:
                rune_name_dict[rune_name_now] += 1

        for key, val in rune_name_dict.items():
            if val > 2:
                gr.Warning("石板属性 " + key + " 不能超过2条！")

