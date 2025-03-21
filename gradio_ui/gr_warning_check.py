"""
用于检测数据合法性
"""

import gradio as gr


def check_glyph(glyph_list):
    filtered_lst = [x for x in glyph_list if x != "无"]

    if len(filtered_lst) != len(set(filtered_lst)):
        print(len(filtered_lst), len(set(filtered_lst)))
        gr.Warning("不能选择重复的纹章！")


