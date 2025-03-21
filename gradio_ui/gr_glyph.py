"""
纹章页
"""

import gradio as gr
import json


def get_glyph_data():
    """ 获取纹章数据 """
    glyph_base_list = ["无"]
    glyph_plus_list = ["无"]

    glyph_base_tmp = []
    # 打开 JSON 文件
    with open('data/glyph.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for lev, em_dic in data["base"].items():
            for em_name, val in em_dic.items():
                glyph_base_tmp.append(lev + "-" + em_name)
        for lev, em_dic in data["plus"].items():
            for em_name, val in em_dic.items():
                glyph_plus_list.append(em_name)
            break

    # 排序 50放前面
    # glyph_base_list = glyph_base_list + sorted(glyph_base_tmp, key=lambda x: int(x[:2]), reverse=True)
    glyph_base_list = glyph_base_list + sorted(glyph_base_tmp)

    return glyph_base_list, glyph_plus_list


def create_glyph_tab():
    """ gr页面 """
    glyph_base_list, glyph_plus_list = get_glyph_data()

    with gr.Tab("纹章页"):
        gr.Markdown("### 基础纹章栏")
        with gr.Row():
            glyph1 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章1")
            glyph1_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章1三属性")
        with gr.Row():
            glyph2 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章2")
            glyph2_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章2三属性")
        with gr.Row():
            glyph3 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章3")
            glyph3_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章3三属性")
        with gr.Row():
            glyph4 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章4")
            glyph4_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章4三属性")
        with gr.Row():
            glyph5 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章5")
            glyph5_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章5三属性")
        with gr.Row():
            glyph6 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章6")
            glyph6_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章6三属性")
        with gr.Row():
            glyph7 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章7")
            glyph7_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章7三属性")
        with gr.Row():
            glyph8 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="纹章8")
            glyph8_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="纹章8三属性")
        gr.Markdown("---")
        gr.Markdown("### 额外纹章栏")
        with gr.Row():
            glyph9 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="额外纹章1")
            glyph9_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="额外纹章1三属性")
        with gr.Row():
            glyph10 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="额外纹章2")
            glyph10_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="额外纹章2三属性")
        with gr.Row():
            glyph11 = gr.Dropdown(glyph_base_list, value=glyph_base_list[0], label="额外纹章3")
            glyph11_p = gr.Dropdown(glyph_plus_list, value=glyph_plus_list[0], label="额外纹章3三属性")

    glyph_list = [glyph1, glyph2, glyph3, glyph4,
                   glyph5, glyph6, glyph7, glyph8,
                   glyph9, glyph10, glyph11]
    glyph_p_list = [glyph1_p, glyph2_p, glyph3_p, glyph4_p,
                     glyph5_p, glyph6_p, glyph7_p, glyph8_p,
                     glyph9_p, glyph10_p, glyph11_p]
    return glyph_list, glyph_p_list
