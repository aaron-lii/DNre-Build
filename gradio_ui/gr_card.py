"""
卡片页
"""

import gradio as gr

from src.tool_func import card_skill_json, card_json


def get_card_data():
    """ 获取卡片数据 """
    card_skill_list = list(card_skill_json.keys())
    card_list = list(card_json.keys())
    return card_skill_list, card_list


def create_card_tab():
    """ gr页面 """
    card_skill_list, card_list = get_card_data()

    card_skill_res_list = []
    card_res_list = []

    with gr.Tab("卡片页"):
        gr.Markdown("### 掌握之力")
        for i in range(len(card_skill_list) // 4):
            with gr.Row():
                for j in range(4):
                    card_skill_levle_now = gr.Slider(minimum=0, maximum=20, value=0, step=1,
                                                     label=card_skill_list[i * 4 + j])
                    card_skill_res_list.append(card_skill_levle_now)

        gr.Markdown("---")
        for i in range(4):
            gr.Markdown(f"### 怪物卡片 第{i + 1}页")
            for j in range(4):
                with gr.Row():
                    for k in range(4):
                        card_i = i * 16 + j * 4 + k
                        if card_i < len(card_list):
                            card_now = gr.Radio(choices=["无", "C", "B", "A", "S", "L"],
                                                label=card_list[card_i],
                                                value="无")
                            card_res_list.append(card_now)

    return card_skill_res_list, card_res_list
